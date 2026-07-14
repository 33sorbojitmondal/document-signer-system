# Generated manually for authority workflow

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signer', '0002_document_file_content_document_original_filename_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.CharField(
                choices=[('user', 'User'), ('authority', 'Authority')],
                default='user',
                max_length=20,
            ),
        ),
        migrations.RenameField(
            model_name='document',
            old_name='uploaded_at',
            new_name='submitted_at',
        ),
        migrations.AddField(
            model_name='document',
            name='reviewed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='status',
            field=models.CharField(
                choices=[
                    ('pending_authority', 'Pending Authority Review'),
                    ('verified', 'Verified by Authority'),
                    ('rejected', 'Rejected'),
                    ('tampered', 'Tampered'),
                ],
                default='pending_authority',
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name='digitalsignature',
            name='signer',
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name='authority_signatures',
                to='auth.user',
            ),
        ),
    ]
