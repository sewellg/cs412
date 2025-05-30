# Generated by Django 5.2.1 on 2025-05-27 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_name',
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image_url',
            field=models.URLField(),
        ),
    ]
