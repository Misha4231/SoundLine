from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.core import serializers
from .models import *
from .forms import *
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.views.generic import View
from django.http import JsonResponse, StreamingHttpResponse
from django.forms.models import model_to_dict
import json
import datetime
import os
from .services import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify


class PlayListsList(ListView):
    model = PlayListHearingHistory
    template_name = 'music/playlists_list.html'

    def get_queryset(self):
        qs= super().get_queryset()
        if self.request.user.is_authenticated:
            qs = PlayListHearingHistory.objects.filter(user=self.request.user).distinct('playList')[:20]
        return qs

class SongList(DetailView):
    model = PlayList
    template_name = 'music/songs_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context['object_list'] = obj.song.all()
        return context


class SongDetail(DetailView):
    model = Song
    template_name = 'music/song_detail.html'
   
def get_streaming_audio(request,slug):
    file,status_code,content_range = open_file(request,slug)
    
    response = StreamingHttpResponse(file, status=status_code, content_type='audio/mp3')
    response['Accept-Ranges'] = 'bytes'
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response

def history_save(request,slug):

    plaulist = PlayList.objects.get(slug=slug)
    PlayListHearingHistory.objects.create(user=request.user,playList=plaulist)
    return JsonResponse({'status': 'ok'})

def plus_hearing(request, slug):
    song = Song.objects.get(slug=slug)
    last_listen_time = request.COOKIES.get('last_listen_time')
    if not last_listen_time or ((datetime.datetime.now() - datetime.timedelta(hours=2)) - datetime.datetime.fromisoformat(last_listen_time)).total_seconds() > 120:
        song.hearings += 1
        song.save()
        expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=2)
        response = JsonResponse({'status': 'ok'})
        response.set_cookie('last_listen_time', datetime.datetime.utcnow().isoformat(), expires=expires)
        return response
    else:
        return JsonResponse({'status': 'error', 'message': 'q'})



class Search(View):
    def get(self,request,*args,**kwargs):
        form = SearchForm()
        return render(request, 'music/search.html', {'form':form})
    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            query = request.POST.get('query')
            
            songs = Song.objects.filter(title__icontains=query)[:7]
            playlists = PlayList.objects.filter(title__icontains=query)[:7]
            songs_serialized = serializers.serialize('json', songs)
            playlists_serialized = serializers.serialize('json', playlists)
            songs_list = json.loads(songs_serialized)
            playlists_list = json.loads(playlists_serialized)
            
            for song in songs_list:
                fields = song['fields']
                fields['pk'] = song['pk']
                fields['link'] = str(reverse('song_detail', args=[fields['slug']]))
            
            for playlist in playlists_list:
                fields = playlist['fields']
                fields['pk'] = playlist['pk']
                fields['link'] = str(reverse('playlist_detail', args=[fields['slug']]))

            
            return JsonResponse({'songs': json.dumps(songs_list), 'playlists': json.dumps(playlists_list)}, status=200)


def song_like(request, slug):
    song = Song.objects.get(slug=slug)
    
    if request.user in song.users_like.all():
        song.users_like.remove(request.user)
        
    else:
        song.users_like.add(request.user)
        
    return JsonResponse({'status':'ok'})


class likedSongs(ListView):
    template_name = 'music/liked_songs.html'
    model = Song

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(users_like__in=[self.request.user])
        return qs


def form_search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        query = request.GET.get('query')
        
        songs = Song.objects.filter(title__icontains=query)
        songs_serialized = serializers.serialize('json', songs)
        songs_list = json.loads(songs_serialized)
        
        for song in songs_list:
            fields = song['fields']
            fields['pk'] = song['pk']
            fields['link'] = str(reverse('song_detail', args=[fields['slug']]))
        
        return JsonResponse({'songs': json.dumps(songs_list)}, status=200)

class EditPlaylistMixin:
    model = PlayList
    success_url = reverse_lazy('playlists_list')
    fields = ['title','image','song']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.cleaned_data.get('title'))

        return super().form_valid(form)

class AddPlaylist(EditPlaylistMixin,CreateView):
    template_name = 'music/add_playlist.html'
    

class UpdatePlaylist(EditPlaylistMixin,UpdateView):
    model = PlayList
    template_name = 'music/update_playlist.html'

class DeletePlaylist(DeleteView):
    model = PlayList
    template_name ='music/delete_playlist.html'
    success_url = reverse_lazy('playlists_list')

class SelfSongsMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context['object_list'] = obj.user.song_authors.all()
        return context

class AlbumsMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context['album_list'] = obj.user.albom_authors.all()
        return context

class ProfileUpdate(AlbumsMixin,SelfSongsMixin,UpdateView):
    model = Profile
    template_name = 'user/profile.html'
    fields = ['avatar','name','description']
    success_url = reverse_lazy('playlists_list')

class ProfileDetail(AlbumsMixin,SelfSongsMixin,DetailView):
    model = Profile
    template_name = 'user/profile-detail.html'

class UserAlbums(ListView):
    model = Album
    template_name = 'music/user-albums.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author=self.request.user)

class EditUserAlbumsMixin:
    model = Album
    fields = ['title','image']
    success_url = reverse_lazy('user_albums')

class UpdateUserAlbum(EditUserAlbumsMixin,UpdateView):
    template_name = 'music/update-user-album.html'
    
class CreateUserAlbum(EditUserAlbumsMixin, CreateView):
    template_name = 'music/create-user-album.html'

    def form_valid(self, form):
        form.instance.slug = slugify(form.cleaned_data.get('title'))
        form.instance.author = self.request.user
        return super().form_valid(form)

class AlbumDetail(DetailView):
    model = Album
    template_name = 'music/user-album-detail.html'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['object_list'] = self.get_object().albom_songs.all()
        return context
    
class CreateSong(CreateView):
    model = Song
    fields = ['title', 'authors', 'album', 'song_file', 'image', 'genre']
    success_url = reverse_lazy('playlists_list')
    template_name = 'music/add_song.html'

    def form_valid(self, form):
        form.instance.slug = slugify(form.cleaned_data['title'])
        form.instance.album = form.cleaned_data['album']
        
        return super().form_valid(form)


def user_search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        query = request.GET.get('query')
        users = User.objects.filter(user_profiles__name__icontains=query)
        users_serialized = serializers.serialize('json', users)
        users_list = json.loads(users_serialized)

        for user in users_list:
            fields = user['fields']
            fields['pk'] = user['pk']
            
        return JsonResponse({'users': json.dumps(users_list)}, status=200)