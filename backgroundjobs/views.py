from django.shortcuts import render
import os
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
# from .forms import UserRegistrationForm
# from .models import Repository, Ssh_key
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .tasks import run_the_container
import json
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from celery.result import AsyncResult


def call_celery(request,repo_path,commit_id):
    task=run_the_container.delay(repo_path,commit_id)
    return 202,{'Location':reverse('check_status')+ task.id}

def check_status(request,task_id):
    task=AsyncResult(task_id)
    state=task.state
    return state