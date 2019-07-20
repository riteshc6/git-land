import os
import sys
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .tasks import run_the_container
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from git_land.models import Test_info,Repository
from django.contrib import messages
from django.contrib.auth.models import User


def call_celery(repo_path,commit_id,commit_message):
    # repo_path='/'+repo_path
    task = run_the_container.delay(repo_path, commit_id,commit_message)
    # return JsonResponse({'Location': reverse('check_status',kwargs={'task_id':task.id}),'status_code':202})
    return True


def check_status(task_id):
    task = run_the_container.AsyncResult(task_id)
    # response = {
    #     'state': task.state
    # }
    # if task.info:
    #     response = {
    #         'state': task.state,
    #         'result': task.info[0]
    #     }


    if task.state == 'PENDING':
        import time
        time.sleep(1)
        return check_status(task_id)
    elif task.state == 'SUCCESS':
        # return display_messages(response['result'])
        return True
    # return JsonResponse(response)

# def display_messages(request, test_id):

#     test_info = get_object_or_404(Test_info, id=test_id)
#     test_exit_code = test_info.test_exit_code
#     test_message = test_info.log

#     if test_exit_code == 0:
#         messages.success(request, 'Test cases have executed successfully.')
#     elif test_exit_code == 1:
#         messages.error(
#             request, 'Error was raised during testing \n{}'.format(test_message))
#     elif test_exit_code == 2:
#         messages.error(
#             request, 'Timed out during the execution of test cases. \n{}'.format(test_message))

#     return render(request, 'notifications.html')


def display_message(request):
    print('ajax call')
    repo_user=get_object_or_404(User,username=request.user.username)
    print(repo_user)
    repos=Repository.objects.filter(user=repo_user).all()
    print(repos)
    new_tests=Test_info.objects.filter(repo__in=repos).filter(new_message=True).all()
    print(new_tests)
    json_message=[]
    for test in new_tests:
        message_dict={}
        if test.test_exit_code == 0:
            message_dict['Result']= 'Test cases have executed successfully.'
        elif test.test_exit_code == 1:
            message_dict['Result']= 'Error was raised during testing.'
        elif test.test_exit_code == 2:
            message_dict['Result']= 'Timed out during the execution of test cases. '
        message_dict['Commit message']=test.commit_message
        message_dict['Commit id']=test.commit_id
        message_dict['Executed at']=test.timestamp
        json_message.append(message_dict)
        test.new_message=False
        test.save()
        print(message_dict)
    print(json_message)
    return JsonResponse(json_message,safe=False)


def display_all_messages(request,username,repo_name):
    user=User.objects.get(username=username)
    repo=Repository.objects.filter(name=repo_name).filter(user=user).first()
    test_info=Test_info.objects.filter(repo=repo).all()
    return render(request,'test-results.html',{'test_info':test_info, 'repo_name':repo_name})


def test_log(request,username,repo_name,test_id):
    test=get_object_or_404(Test_info,id=test_id)
    return render(request,'testlog.html',{'test':test})

if __name__=='__main__':
    call_celery(sys.argv[1],sys.argv[2],sys.argv[3])

