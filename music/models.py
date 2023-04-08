from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user_profiles')
    avatar = models.ImageField(upload_to='profiles/%Y/%m/%d/', default='default/default-avatar.jpg')
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255)
    description = models.CharField(max_length=2000)
    favorite_genres = models.ManyToManyField(Genre, related_name='profile_genres', blank=True)

    def __str__(self) -> str:
        return self.name

    
class Album(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(User, related_name='albom_authors', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='albom/%Y/%m/%d/', unique=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

class Song(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(User, related_name='song_authors')
    hearings = models.PositiveIntegerField(default=0)
    album = models.ForeignKey(Album, related_name='albom_songs', on_delete=models.CASCADE)
    song_file = models.FileField(upload_to='song/%Y/%m/%d/', unique=True)
    image = models.ImageField(upload_to='song_images/%Y/%m/%d/', unique=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True)
    genre = models.ForeignKey(Genre, related_name='genres', on_delete=models.CASCADE, blank=True, null=True)
    users_like = models.ManyToManyField(User,related_name='image_liked',blank=True)

    def __str__(self) -> str:
        return self.title
    

class PlayList(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, related_name='playlist_authors', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='playlist/%Y/%m/%d/', unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    song = models.ManyToManyField(Song, related_name='playlist_songs')
    
    
    def __str__(self) -> str:
        return self.title
    
class PlayListHearingHistory(models.Model):
    user = models.ForeignKey(User, related_name='user_hearing', on_delete=models.CASCADE)
    playList = models.ForeignKey(PlayList, related_name='heared_playlist', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.playList.title