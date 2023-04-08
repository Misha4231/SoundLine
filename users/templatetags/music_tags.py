from django import template
from music.models import *

register = template.Library()

@register.simple_tag(takes_context=True)
def get_self_albums(context):
    return Album.objects.filter(author=context['request'].user)

@register.simple_tag()
def get_all_genres():
    return Genre.objects.all()

@register.simple_tag()
def get_all_users():
    return User.objects.all()

@register.simple_tag()
def get_all_songs():
    return Song.objects.all()

@register.simple_tag(takes_context=True)
def get_user_playlists(context):
    return PlayList.objects.filter(author=context['request'].user)

@register.simple_tag(takes_context=True)
def get_profie(context):
    return Profile.objects.get(user=context['request'].user)

@register.simple_tag()
def get_last_playlists():
    return PlayList.objects.all()[:15]