# Generated by Django 4.2.7 on 2025-02-25 19:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creation Date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='useraccount',
            name='update_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Update Date'),
        ),
    ]
