from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        })
    )


class DocumentUploadForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Document Title',
        })
    )
    file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.txt,.doc,.docx,.png,.jpg,.jpeg',
        })
    )


class VerifyDocumentForm(forms.Form):
    document_id = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Document ID',
        })
    )
