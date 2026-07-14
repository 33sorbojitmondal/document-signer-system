from django.contrib import admin

from .models import DigitalSignature, Document, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__username']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'status', 'uploaded_at']
    list_filter = ['status', 'uploaded_at']
    search_fields = ['title', 'owner__username']


@admin.register(DigitalSignature)
class DigitalSignatureAdmin(admin.ModelAdmin):
    list_display = ['document', 'signer', 'algorithm', 'signed_at']
    search_fields = ['document__title', 'signer__username']
