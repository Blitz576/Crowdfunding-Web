# Generated by Django 5.0.4 on 2024-04-12 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_user_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(default=1, max_length=225),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='facebook',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, default='images/user/default.jpg', upload_to='images/user'),
        ),
    ]
