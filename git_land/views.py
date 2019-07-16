import os
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm
from .models import Repository, Ssh_key
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
@login_required
def home(request):
    username = request.user.username
    return redirect('repos_home', username=username)


@login_required
def repos(request, username, filepath):
    user = request.user
    path = request.path
    username = user.username
    repos = os.listdir('/'+filepath)
    print(repos)
    return render(request, 'git_land/repos.html', {'repos': repos, 'filepath': filepath})


@login_required
def repos_home(request, username):
    user = request.user
    path = request.path
    username = user.username
    repos = os.listdir('/')
    print(repos)
    return render(request, 'git_land/repos.html', {'repos': repos, 'filepath': 'home'})


def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('repos', username=username)
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})
