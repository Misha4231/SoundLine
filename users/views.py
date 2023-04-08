from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, User,Profile
from django.contrib.auth import login,authenticate
from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.edit import CreateView
from django.utils.text import slugify

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile_create')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],password=cd['password2'])
        login(self.request, user)
        return result
    
class ProfileView(CreateView):
    model = Profile
    template_name = 'registration/profile_create.html'
    success_url = '/'
    fields = ('name','avatar','description')

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.slug = slugify(profile.name)
        profile.save()
        return super().form_valid(form)