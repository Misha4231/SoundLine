# Generated by Django 4.1.7 on 2023-03-26 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_song_slug_alter_album_slug_alter_playlist_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
