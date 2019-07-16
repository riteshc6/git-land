import os
import subprocess
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, RepoForm
from .models import Repository, Ssh_key, Repository
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
    repos = os.listdir('/home')
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
            return redirect('repos_home', username=username)
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def repo_form(request, username):
    if request.method == 'POST':
        form = RepoForm(request.POST)
        if form.is_valid():
            username = request.user.username
            repo_data = Repository()
            repo_name = form.cleaned_data['repo_name']
            subprocess.run(
                ['./create_repo.sh', username, repo_name])
            repo_path = '~/users/'+username+repo_name
            repo_data.user = request.user
            repo_data.repo_path = repo_path
            repo_data.save()
            redirect('repos_home', user=username)
    else:
        form = RepoForm()
        return render(request, 'git_land/repo_form.html', {'form': form, 'user': request.user})
