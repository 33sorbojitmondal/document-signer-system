from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Extended user profile with RSA cryptographic keys and role."""

    ROLE_CHOICES = [
        ('user', 'User'),
        ('authority', 'Authority'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    private_key = models.TextField(help_text='RSA private key (PEM format)')
    public_key = models.TextField(help_text='RSA public key (PEM format)')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} ({self.get_role_display()})'

    @property
    def is_authority(self):
        return self.role == 'authority'


class Document(models.Model):
    """Uploaded document metadata and file reference."""

    STATUS_CHOICES = [
        ('pending_authority', 'Pending Authority Review'),
        ('verified', 'Verified by Authority'),
        ('rejected', 'Rejected'),
        ('tampered', 'Tampered'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/', blank=True, null=True)
    file_content = models.BinaryField(blank=True, null=True)
    original_filename = models.CharField(max_length=255, blank=True)
    file_hash = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_authority')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-submitted_at']

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
    """Authority digital signature record for a verified document."""

    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name='signature')
    signer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authority_signatures')
    signature_data = models.TextField(help_text='Base64-encoded RSA signature')
    document_hash = models.CharField(max_length=64)
    algorithm = models.CharField(max_length=50, default='RSA-2048-PSS-SHA256')
    signed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Authority signature for {self.document.title}'

    @property
    def authority(self):
        return self.signer
