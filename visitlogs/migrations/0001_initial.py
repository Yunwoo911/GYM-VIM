# Generated by Django 5.0.6 on 2024-07-30 16:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gyms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitLog',
            fields=[
                ('visitlog_id', models.AutoField(primary_key=True, serialize=False)),
                ('nfc_uid', models.CharField(max_length=30, null=True)),
                ('enter_time', models.DateTimeField()),
                ('exit_time', models.DateTimeField(null=True)),
                ('QR_fields', models.CharField(max_length=100, null=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gyms.gymmember')),
            ],
        ),
    ]
