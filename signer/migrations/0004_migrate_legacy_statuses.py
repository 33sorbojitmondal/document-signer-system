from django.db import migrations


def migrate_document_statuses(apps, schema_editor):
    Document = apps.get_model('signer', 'Document')
    status_map = {
        'uploaded': 'pending_authority',
        'signed': 'verified',
    }
    for old_status, new_status in status_map.items():
        Document.objects.filter(status=old_status).update(status=new_status)


class Migration(migrations.Migration):

    dependencies = [
        ('signer', '0003_authority_workflow'),
    ]

    operations = [
        migrations.RunPython(migrate_document_statuses, migrations.RunPython.noop),
    ]
