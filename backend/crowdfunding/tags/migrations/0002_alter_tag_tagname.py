# Generated by Django 5.0.4 on 2024-04-15 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='tagName',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]