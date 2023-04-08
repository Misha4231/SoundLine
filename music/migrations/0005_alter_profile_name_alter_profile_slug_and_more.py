# Generated by Django 4.1.7 on 2023-03-26 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_profile_name_profile_slug_alter_song_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='profile',
            name='slug',
            field=models.SlugField(max_length=255),
        ),
        migrations.AlterField(
            model_name='song',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
