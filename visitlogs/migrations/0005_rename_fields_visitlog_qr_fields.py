# Generated by Django 5.0.4 on 2024-07-30 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visitlogs', '0004_remove_visitlog_fields_visitlog_qr_fields'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visitlog',
            old_name='fields',
            new_name='QR_fields',
        ),
    ]
