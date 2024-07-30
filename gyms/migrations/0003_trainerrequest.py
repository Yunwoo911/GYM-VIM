# Generated by Django 5.0.6 on 2024-07-30 15:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gyms', '0002_remove_trainer_owner_trainer_user_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainerRequest',
            fields=[
                ('trainer_request_id', models.AutoField(primary_key=True, serialize=False)),
                ('request_date', models.DateField(blank=True, null=True)),
                ('request_message', models.TextField(blank=True, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('approved_date', models.DateField(blank=True, null=True)),
                ('reject_reason', models.TextField(blank=True, null=True)),
                ('approved_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='gyms.owner')),
                ('requested_gym', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gyms.gym')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='trainer',
            name='owner',
        ),
        migrations.AddField(
            model_name='trainer',
            name='user',
            field=models.OneToOneField(limit_choices_to={'usertype': 1}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
