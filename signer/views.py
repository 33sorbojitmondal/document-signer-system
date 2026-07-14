from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .crypto_utils import (
    compute_document_hash,
    generate_rsa_key_pair,
    serialize_private_key,
    serialize_public_key,
    sign_document,
    verify_document_signature,
)
from .decorators import authority_required, user_required
from .forms import DocumentUploadForm, LoginForm, RegisterForm
from .models import DigitalSignature, Document, UserProfile


def _redirect_by_role(user):
    if hasattr(user, 'profile') and user.profile.is_authority:
        return redirect('authority_dashboard')
    return redirect('dashboard')


def home_view(request):
    if request.user.is_authenticated:
        return _redirect_by_role(request.user)
    return render(request, 'signer/home.html')


def register_view(request):
    if request.user.is_authenticated:
        return _redirect_by_role(request.user)

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            private_key, public_key = generate_rsa_key_pair()
            UserProfile.objects.create(
                user=user,
                role='user',
                private_key=serialize_private_key(private_key),
                public_key=serialize_public_key(public_key),
            )
            login(request, user)
            messages.success(request, 'Account created. You can now upload documents for authority verification.')
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'signer/register.html', {'form': form})


def user_login_view(request):
    if request.user.is_authenticated:
        return _redirect_by_role(request.user)

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not hasattr(user, 'profile') or user.profile.is_authority:
                messages.error(request, 'Please use the Authority Login portal.')
                return redirect('authority_login')
            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'signer/login_user.html', {'form': form})


def authority_login_view(request):
    if request.user.is_authenticated:
        return _redirect_by_role(request.user)

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not hasattr(user, 'profile') or not user.profile.is_authority:
                messages.error(request, 'Please use the User Login portal.')
                return redirect('user_login')
            login(request, user)
            messages.success(request, 'Authority access granted.')
            return redirect('authority_dashboard')
        messages.error(request, 'Invalid authority credentials.')
    else:
        form = LoginForm()

    return render(request, 'signer/login_authority.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@user_required
def dashboard_view(request):
    documents = Document.objects.filter(owner=request.user)
    upload_form = DocumentUploadForm()

    if request.method == 'POST':
        upload_form = DocumentUploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            uploaded_file = request.FILES['file']
            file_content = uploaded_file.read()
            doc_kwargs = {
                'owner': request.user,
                'title': upload_form.cleaned_data['title'],
                'file_content': file_content,
                'original_filename': uploaded_file.name,
                'file_hash': compute_document_hash(file_content).hex(),
                'status': 'pending_authority',
            }
            if not getattr(settings, 'VERCEL', False):
                uploaded_file.seek(0)
                doc_kwargs['file'] = uploaded_file
            doc = Document.objects.create(**doc_kwargs)
            messages.success(
                request,
                f'Document "{doc.title}" submitted to authority for verification.',
            )
            return redirect('dashboard')

    return render(request, 'signer/dashboard.html', {
        'documents': documents,
        'upload_form': upload_form,
    })


@authority_required
def authority_dashboard_view(request):
    pending = Document.objects.filter(status='pending_authority')
    reviewed = Document.objects.exclude(status='pending_authority').order_by('-reviewed_at')[:10]
    return render(request, 'signer/authority_dashboard.html', {
        'pending_documents': pending,
        'reviewed_documents': reviewed,
    })


@authority_required
def authority_verify_sign_view(request, doc_id):
    document = get_object_or_404(Document, id=doc_id, status='pending_authority')

    if request.method == 'POST' and request.POST.get('action') == 'reject':
        document.status = 'rejected'
        document.reviewed_at = timezone.now()
        document.save()
        messages.warning(request, f'Document "{document.title}" has been rejected.')
        return redirect('authority_dashboard')

    file_content = document.get_file_content()
    profile = request.user.profile
    signature_b64, doc_hash = sign_document(profile.private_key, file_content)

    DigitalSignature.objects.create(
        document=document,
        signer=request.user,
        signature_data=signature_b64,
        document_hash=doc_hash,
    )
    document.status = 'verified'
    document.file_hash = doc_hash
    document.reviewed_at = timezone.now()
    document.save()

    messages.success(
        request,
        f'Document "{document.title}" verified and signed with authority digital signature.',
    )
    return redirect('authority_dashboard')


@authority_required
def authority_document_detail_view(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    signature = getattr(document, 'signature', None)
    return render(request, 'signer/authority_document_detail.html', {
        'document': document,
        'signature': signature,
    })


@user_required
def verify_document_view(request, doc_id):
    document = get_object_or_404(Document, id=doc_id, owner=request.user)
    result = None

    if not hasattr(document, 'signature'):
        messages.error(request, 'This document has not been verified by authority yet.')
        return redirect('dashboard')

    file_content = document.get_file_content()
    sig = document.signature
    authority_profile = sig.authority.profile

    is_valid = verify_document_signature(
        authority_profile.public_key,
        file_content,
        sig.signature_data,
    )
    current_hash = compute_document_hash(file_content).hex()
    is_tampered = current_hash != sig.document_hash

    if is_valid and not is_tampered:
        result = 'valid'
        messages.success(request, 'Authority signature verified. Document is authentic.')
    elif is_tampered:
        document.status = 'tampered'
        document.save()
        result = 'tampered'
        messages.error(request, 'Tampering detected! Document has been modified after authority signing.')
    else:
        result = 'invalid'
        messages.error(request, 'Authority signature verification failed.')

    return render(request, 'signer/verify.html', {
        'document': document,
        'signature': sig,
        'result': result,
    })


@user_required
def document_detail_view(request, doc_id):
    document = get_object_or_404(Document, id=doc_id, owner=request.user)
    signature = getattr(document, 'signature', None)
    return render(request, 'signer/document_detail.html', {
        'document': document,
        'signature': signature,
    })


@login_required
def legacy_login_redirect(request):
    return _redirect_by_role(request.user)
