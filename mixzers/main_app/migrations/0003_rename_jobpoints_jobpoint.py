# Generated by Django 4.1.7 on 2023-04-05 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_jobpoints'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='JobPoints',
            new_name='JobPoint',
        ),
    ]
