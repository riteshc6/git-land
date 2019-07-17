import os
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .tasks import run_the_container
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
# from celery.result import AsyncResult
from django.http import JsonResponse
from git_land.models import Test_info,Repository
from django.contrib import messages


def take_the_control(repo_path,commit_id):
    # call_celery(repo_path,commit_id)
    pass

def call_celery(request,repo_path,commit_id):
    repo_path='/'+repo_path
    task = run_the_container.delay(repo_path, commit_id)
    return JsonResponse({'Location': reverse('check_status',kwargs={'task_id':task.id}),'status_code':202})
    # return check_status(request,task.id)


def check_status(request, task_id):
    task = run_the_container.AsyncResult(task_id)
    response = {
        'state': task.state
    }
    if task.info:
        response = {
            'state': task.state,
            'result': task.info[0]
        }

    # if task.state == 'PENDING':
    #     return check_status(request, task_id)
    # elif task.state == 'SUCCESS':
    #     return display_messages(request, response['result'])

    return JsonResponse(response)

def display_messages(request, test_id):

    test_info = get_object_or_404(Test_info, id=test_id)
    test_exit_code = test_info.test_exit_code
    test_message = test_info.log

    if test_exit_code == 0:
        messages.success(request, 'Test cases have executed successfully.')
    elif test_exit_code == 1:
        messages.error(
            request, 'Error was raised during testing \n{}'.format(test_message))
    elif test_exit_code == 2:
        messages.error(
            request, 'Timed out during the execution of test cases. \n{}'.format(test_message))

    return render(request, 'notifications.html')

def display_all_messages(request,username,repo_id):
    # repo=Repository.objects.get(id=repo_id)
    test_info=Test_info.objects.all()
    return render(request,'test-results.html',{'test_info':test_info, 'repo_id':repo_id})

def  test(request):
    return render(request,'test.html')
