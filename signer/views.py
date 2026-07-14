from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .crypto_utils import (
    compute_document_hash,
    generate_rsa_key_pair,
    serialize_private_key,
    serialize_public_key,
    sign_document,
    verify_document_signature,
)
from .forms import DocumentUploadForm, LoginForm, RegisterForm, VerifyDocumentForm
from .models import DigitalSignature, Document, UserProfile


def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            private_key, public_key = generate_rsa_key_pair()
            UserProfile.objects.create(
                user=user,
                private_key=serialize_private_key(private_key),
                public_key=serialize_public_key(public_key),
            )
            login(request, user)
            messages.success(request, 'Account created successfully. RSA key pair generated.')
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'signer/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Welcome back!')
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'signer/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
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
            }
            if not getattr(settings, 'VERCEL', False):
                uploaded_file.seek(0)
                doc_kwargs['file'] = uploaded_file
            doc = Document.objects.create(**doc_kwargs)
            messages.success(request, f'Document "{doc.title}" uploaded successfully.')
            return redirect('dashboard')

    return render(request, 'signer/dashboard.html', {
        'documents': documents,
        'upload_form': upload_form,
    })


@login_required
def sign_document_view(request, doc_id):
    document = get_object_or_404(Document, id=doc_id, owner=request.user)

    if hasattr(document, 'signature'):
        messages.warning(request, 'This document is already signed.')
        return redirect('dashboard')

    file_content = document.get_file_content()

    profile = request.user.profile
    signature_b64, doc_hash = sign_document(profile.private_key, file_content)

    DigitalSignature.objects.create(
        document=document,
        signer=request.user,
        signature_data=signature_b64,
        document_hash=doc_hash,
    )
    document.status = 'signed'
    document.file_hash = doc_hash
    document.save()

    messages.success(request, f'Document "{document.title}" signed successfully with RSA-2048.')
    return redirect('dashboard')


@login_required
def verify_document_view(request, doc_id=None):
    result = None
    document = None
    form = VerifyDocumentForm()

    if doc_id:
        document = get_object_or_404(Document, id=doc_id, owner=request.user)
        form = VerifyDocumentForm(initial={'document_id': doc_id})

    if request.method == 'POST':
        form = VerifyDocumentForm(request.POST)
        if form.is_valid():
            document = get_object_or_404(
                Document,
                id=form.cleaned_data['document_id'],
                owner=request.user,
            )

            if not hasattr(document, 'signature'):
                messages.error(request, 'This document has not been signed yet.')
                return redirect('verify')

            file_content = document.get_file_content()

            sig = document.signature
            is_valid = verify_document_signature(
                request.user.profile.public_key,
                file_content,
                sig.signature_data,
            )

            current_hash = compute_document_hash(file_content).hex()
            is_tampered = current_hash != sig.document_hash

            if is_valid and not is_tampered:
                document.status = 'verified'
                result = 'valid'
                messages.success(request, 'Signature verified. Document is authentic and untampered.')
            elif is_tampered:
                document.status = 'tampered'
                result = 'tampered'
                messages.error(request, 'Tampering detected! Document hash does not match signed hash.')
            else:
                result = 'invalid'
                messages.error(request, 'Signature verification failed.')
            document.save()

    return render(request, 'signer/verify.html', {
        'form': form,
        'document': document,
        'result': result,
    })


@login_required
def document_detail_view(request, doc_id):
    document = get_object_or_404(Document, id=doc_id, owner=request.user)
    signature = getattr(document, 'signature', None)
    return render(request, 'signer/document_detail.html', {
        'document': document,
        'signature': signature,
    })
