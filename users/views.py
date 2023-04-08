from django.shortcuts import render,redirect
from django.urls import reverse_lazy

from .forms import UserRegistrationForm, User,Profile
from django.contrib.auth import login,authenticate
from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.edit import CreateView
from django.utils.text import slugify


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            user = authenticate(username=user_form.cleaned_data['username'],password=user_form.cleaned_data['password2'])
            login(request, user)
            return redirect('profile_create')
    else:
        user_form = UserRegistrationForm()
    return render(request,'registration/register.html',{'form':user_form})
    
    
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