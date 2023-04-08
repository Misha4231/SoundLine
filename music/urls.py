from .views import *
from django.urls import path


urlpatterns = [
    path('song_detail/<slug:slug>/', SongDetail.as_view(), name='song_detail'),
    path('playlist_detail/<slug:slug>/', SongList.as_view(), name='playlist_detail'),
    path('stream/<slug:slug>/', get_streaming_audio, name='stream'),
    path('hearing/<slug:slug>', plus_hearing, name='hear'),
    path('search/', Search.as_view(), name='search'),
    path('like/<slug:slug>', song_like, name='like'),
    path('liked_songs/', likedSongs.as_view(), name='liked_songs'),
    path('add_playlist/', AddPlaylist.as_view(), name='add_playlist'),
    path('form_search/', form_search, name='form_search'),
    path('update_playlist/<slug:slug>/', UpdatePlaylist.as_view(), name='update_playlist'),
    path('delte_playlist/<slug:slug>/', DeletePlaylist.as_view(), name='delete_playlist'),
    path('profile/<int:pk>/', ProfileUpdate.as_view(), name='profile'),
    path('profile_detail/<int:pk>/', ProfileDetail.as_view(), name='profile_detail'),
    path('user_albums/', UserAlbums.as_view(), name='user_albums'),
    path('user_album_update/<slug:slug>', UpdateUserAlbum.as_view(), name='user_album_update'),
    path('create_album/', CreateUserAlbum.as_view(), name='create_album'),
    path('album_detail/<slug:slug>/', AlbumDetail.as_view(), name='album_detail'),
    path('add_song/', CreateSong.as_view(), name='add_song'),
    path('user_search/', user_search, name='user_search'),
    path('history_save/<slug:slug>/', history_save,name='history_save')
]

