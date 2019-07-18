import os
import subprocess
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, RepoForm
from .models import Repository, Ssh_key, Repository
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from mysite import settings
from django.contrib import messages

# Create your views here.


@login_required
def home(request):
    username = request.user.username
    return redirect('repos_home', username=username)
    # return render(request, 'git_land/home.html', {})


def landing_page(request):
    if request.user.is_authenticated:
        return redirect('repos_home', username=request.user.username)
    return render(request, 'git_land/home.html', {})


@login_required
def repos(request, username, filepath):
    user = request.user
    path = request.path
    username = user.username
    base_dir = str(filepath).split('/')[:1]
    repo_name = str(filepath).split('/')[1]
    repos_dir = []
    repos_file = []
    try:
        for entry in os.scandir('/'+filepath):
            if entry.is_file():
                print(entry.name)
                repos_file.append(entry.name)
        for entry in os.scandir('/'+filepath):
            if entry.is_dir():
                print(entry.name)
                repos_dir.append(entry.name)
    except FileNotFoundError:
        raise Http404("Poll does not exist")

    return render(request, 'git_land/repos.html', {'repos_dir': repos_dir, 'repos_file': repos_file, 'filepath': filepath, 'repo_name': repo_name})


@login_required
def repo_file(request, username, filepath):
    user = request.user
    username = user.username
    try:
        with open('/'+filepath, 'r') as f:
            content = f.read()
    except FileNotFoundError or NotADirectoryError:
        messages.error(request, 'path does not exists')
        return redirect('repos_home', username=username)

    extension = os.path.splitext('/'+filepath)[1]
    ext_type = settings.extension_mapping[extension]
    return render(request, 'git_land/repo_file.html', {'content': content, 'ext_type': ext_type})


@login_required
def repos_home(request, username):
    user = request.user
    path = request.path
    username = user.username
    repos = os.listdir('/home/gitlab/' + username)
    print(repos)
    repos_file = []
    repos_dir = []
    base_path = 'home/gitlab/' + username'
    for entry in os.scandir('/'+base_path):
        if entry.is_file():
            print(entry.name)
            repos_file.append(entry.name)
    for entry in os.scandir('/'+base_path):
        if entry.is_dir():
            print(entry.name)
            repos_dir.append(entry.name)
    return render(request, 'git_land/repos.html', {'repos_dir': repos_dir, 'repos_file': repos_file, 'filepath': base_path})


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
            repo_path = '/home/gitlab/' + username + '/' + repo_name
            repo_data.user = request.user
            repo_data.name = repo_name
            repo_data.repo_path = repo_path
            repo_data.last_update = timezone.now()
            repo_data.save()
            return redirect('repos_home', username=username)
        return redirect('repo_form', username=username)
    else:
        form = RepoForm()
        return render(request, 'git_land/repo_form.html', {'form': form, 'user': request.user})
