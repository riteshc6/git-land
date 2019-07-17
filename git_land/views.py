import os
import subprocess
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, RepoForm
from .models import Repository, Ssh_key, Repository
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from mysite import settings

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
    repos_file = []
    repos_dir = []
    for entry in os.scandir('/'+filepath):
        if entry.is_file():
            print(entry.name)
            repos_file.append(entry.name)
    for entry in os.scandir('/'+filepath):
        if entry.is_dir():
            print(entry.name)
            repos_dir.append(entry.name)

    return render(request, 'git_land/repos.html', {'repos_dir': repos_dir, 'repos_file': repos_file, 'filepath': filepath})


@login_required
def repo_file(request, username, filepath):
    user = request.user
    username = user.username
    extension = os.path.splitext('/'+filepath)[1]
    
    with open('/'+filepath, 'r') as f:
        content = f.read()

    return render(request, 'git_land/repo_file.html', {'content': content})


@login_required
def repos_home(request, username):
    user = request.user
    path = request.path
    username = user.username
    repos = os.listdir('/home/gitlab/'+username)
    print(repos)
    repos_file = []
    repos_dir = []
    for entry in os.scandir('/home/gitlab/'+username):
        if entry.is_file():
            print(entry.name)
            repos_file.append(entry.name)
    for entry in os.scandir('/home/gitlab/'+username):
        if entry.is_dir():
            print(entry.name)
            repos_dir.append(entry.name)
    return render(request, 'git_land/repos.html', {'repos_dir': repos_dir, 'repos_file': repos_file, 'filepath': '/home/gitlab/'+username})


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
            repo_data.last_update = timezone.now()
            repo_data.save()
            return redirect('repos_home', username=username)
    else:
        form = RepoForm()
        return render(request, 'git_land/repo_form.html', {'form': form, 'user': request.user})
