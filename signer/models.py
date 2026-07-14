from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Extended user profile with RSA cryptographic keys."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    private_key = models.TextField(help_text='RSA private key (PEM format)')
    public_key = models.TextField(help_text='RSA public key (PEM format)')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Profile: {self.user.username}'


class Document(models.Model):
    """Uploaded document metadata and file reference."""

    STATUS_CHOICES = [
        ('uploaded', 'Uploaded'),
        ('signed', 'Signed'),
        ('verified', 'Verified'),
        ('tampered', 'Tampered'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/', blank=True, null=True)
    file_content = models.BinaryField(blank=True, null=True)
    original_filename = models.CharField(max_length=255, blank=True)
    file_hash = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploaded')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f'{self.title} ({self.owner.username})'

    def get_file_content(self):
        """Return document bytes from database or filesystem."""
        if self.file_content:
            return bytes(self.file_content)
        if self.file:
            with self.file.open('rb') as f:
                return f.read()
        return b''


class DigitalSignature(models.Model):
    """Digital signature record for a signed document."""

    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name='signature')
    signer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='signatures')
    signature_data = models.TextField(help_text='Base64-encoded RSA signature')
    document_hash = models.CharField(max_length=64)
    algorithm = models.CharField(max_length=50, default='RSA-2048-PSS-SHA256')
    signed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Signature for {self.document.title}'
