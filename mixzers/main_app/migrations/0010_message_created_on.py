# Generated by Django 4.1.7 on 2023-04-03 16:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_rename_recipient_id_message_recipient_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]