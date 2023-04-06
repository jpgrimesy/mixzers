# Generated by Django 4.1.7 on 2023-04-05 19:02

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobPoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', django.contrib.gis.db.models.fields.PointField(geography=True, srid=4326)),
                ('job_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.job_post')),
            ],
        ),
    ]