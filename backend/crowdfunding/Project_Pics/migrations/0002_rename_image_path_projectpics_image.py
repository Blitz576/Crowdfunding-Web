# Generated by Django 5.0.4 on 2024-04-14 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Project_Pics', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectpics',
            old_name='image_path',
            new_name='image',
        ),
    ]
