from django.contrib import admin
from .models import *

@admin.register(PlayList)
class PlayListAdmin(admin.ModelAdmin):
    fields = ('title','author','image','slug', 'song')
    prepopulated_fields = {'slug': ('title',)}
    

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    fields = ('title','slug','authors','hearings','album','song_file','image','genre','users_like')
    
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    fields = ('title','slug','author','image')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'avatar','description','slug','name')
    prepopulated_fields = {"slug": ('name',)}

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    fields = ('name','slug')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(PlayListHearingHistory)