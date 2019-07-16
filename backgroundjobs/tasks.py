from __future__ import absolute_import,unicode_literals
from celery.decorators import task
import os
import subprocess
from .models import Test_info

@task(name='unit-testing')
def run_the_container(repo_id,commit_id):

    repo_path='/home/ubuntu/docker_test_ci/ci'
    proc = subprocess.run(['./backgroundjobs/ci.sh'],stdout=subprocess.PIPE,cwd=repo_path)
    test_info=Test_info(commit_id=commit_id,commit_message='123',test_exit_code=proc.returncode,log=proc.stdout.decode('utf-8'))
    test_info.save()

    return "exited the worker"    