import os
import traceback
import subprocess
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, RepoForm,OauthRegistrationForm,SshForm
from .models import Repository, Ssh_key, Test_info
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from mysite import settings
from django.contrib import messages

# Create your views here.

def oauth_signup(request):
    if request.method == 'POST':
        form = OauthRegistrationForm(request.POST)
        if form.is_valid():
            form.save() 
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('check_ssh_key')
    else:
        form = OauthRegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def check_ssh_key(request):
    user=get_object_or_404(User,username=request.user.username)
    ssh=Ssh_key.objects.filter(user=user).first()
    if ssh is None:
        if request.method == 'POST':
            form=SshForm(request.POST)
            if form.is_valid():
                ssh_key = Ssh_key()
                ssh_key.key_name = form.cleaned_data['key_name']
                ssh_key.ssh_key = form  .cleaned_data['ssh_key']
                ssh_key.user=request.user
                ssh_key.save()
                subprocess.run(['./create_user.sh', ssh_key.ssh_key, request.user.username])
                return redirect('home')
            else:
                return render(request,'registration/ssh.html',{'form':form})   
        else:
            form = SshForm()
        return render(request,'registration/ssh.html',{'form':form})
    else:
        return redirect('home')
        


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
    list_path = list_of_file_tuples(filepath)
    print(list_path)
    base_path = str(filepath).split('/')[:2]
    path_tree = str(filepath).split('/')[3:]
    repo_name = str(filepath).split('/')[4]
    last_name = str(filepath).split('/')[-1:][0]
    repos_dir = []
    repos_file = []
    md_present = False
    content = None
    try:
        for entry in os.scandir('/'+filepath):
            if entry.is_file():
                print(entry.name)
                if entry.name.endswith("README.md") and md_present == False:
                    with open('/'+filepath+'/'+entry.name, 'r') as f:
                        content = f.read()
                    md_present = True
                proc = subprocess.run(['./time_commit.sh', entry.name, filepath], stdout=subprocess.PIPE)
                proc_out = proc.stdout.decode('utf-8').split('|')
                last_commit_message = proc_out[1]
                last_update = proc_out[0]
                repos_file.append((entry.name,last_commit_message, last_update))

            elif entry.is_dir() and not entry.name.endswith(".git"):
                print(entry.name)
                proc = subprocess.run(['./time_commit.sh', entry.name, filepath], stdout=subprocess.PIPE)    
                proc_out = proc.stdout.decode('utf-8').split('|')
                last_commit_message = proc_out[1]
                last_update = proc_out[0]
                repos_dir.append((entry.name,last_commit_message, last_update))
    except Exception:
        print(Exception)
        traceback.print_exc()
        raise Http404("Poll does not exist")
    
    if len(repos_dir) == 0 and len(repos_file) == 0:
       url = "gitlab@13.233.153.31:" + username + "/" + repo_name + ".git"
       return render(request, 'git_land/new_repo.html', {'url': url,'repo_name':repo_name})
    print(filepath)
    print('repos_dir',repos_dir,'-------------->  ','repos_file', repos_file)
    return render(request, 'git_land/repos.html', {'repos_dir': repos_dir, 'repos_file': repos_file, 'filepath': filepath, 'repo_name': repo_name, 'last_name': last_name, 'md_present': md_present, 'content':content, 'path_tree': path_tree, 'base_path': base_path, 'list_path': list_path})


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
    file_name = str(filepath).split('/')[-1:][0]
    extension = os.path.splitext('/'+filepath)[1]
    ext_type = settings.extension_mapping.get(extension)
    if ext_type is None:
        ext_type = ""
    list_path = list_of_file_tuples(filepath)
    return render(request, 'git_land/repo_file.html', {'content': content, 'ext_type': ext_type, 'file_name': file_name, 'list_path': list_path})


@login_required
def repos_home(request, username):
    user = request.user
    path = request.path
    username = user.username
    all_repos = user.repositories.all()
    repos = os.listdir('/home/gitlab/' + username)
    print(repos)
    repos_file = []
    repos_dir = []
    base_path = 'home/gitlab/' + username
    # for entry in os.scandir('/'+base_path):
    #     if entry.is_file():
    #         print(entry.name)
    #         repos_file.append(entry.name)
    # for entry in os.scandir('/'+base_path):
    #     if entry.is_dir() and not entry.name.endswith(".git"):
    #         print(entry.name)
    #         repos_dir.append(entry.name)
    return render(request, 'git_land/repos.html', {'all_repos':all_repos, 'repos_dir': repos_dir, 'repos_file': repos_file, 'filepath': base_path})


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
            repo_path = '/home/gitlab/' + username + '/' + repo_name
            repo_data.user = request.user
            repo_data.name = repo_name
            repo_data.repo_path = repo_path
            repo_data.last_update = timezone.now()
            repo_data.save()
            subprocess.run(
                ['./create_repo.sh', username, repo_name], stdout=subprocess.PIPE)
            # return redirect('repos_home', username=username)
            # url = "gitlab@13.233.153.31:" + username + "/" + repo_name + ".git"
            return redirect('repos', username = username, filepath = repo_path)
            # return render(request, 'git_land/new_repo.html', {'url': url,'repo_name':repo_name})
        return redirect('repo_form', username=username)
    else:
        form = RepoForm()
        return render(request, 'git_land/repo_form.html', {'form': form, 'user': request.user})


def list_of_file_tuples(filepath):
    list_of_tuples=[]
    all_dirs = str(filepath).split('/')
    base_dirs = str(filepath).split('/')[:4]
    print(base_dirs)
    base_path = base_dirs[0]+'/'+base_dirs[1]+'/'+base_dirs[2]+ '/' + base_dirs[3]
    path_tree = str(filepath).split('/')[4:]
    path = base_path
    i=0
    for file_name in path_tree:
        path = path + '/'  + file_name
        list_of_tuples.append((path_tree[i],path))
        i=i+1

    return list_of_tuples
