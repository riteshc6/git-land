from __future__ import absolute_import,unicode_literals
from celery.decorators import task
import os
import subprocess
from git_land.models import Test_info
# from .models import Test_info

@task(name='unit-testing')
def run_the_container(repo_id,commit_id):

    repo_path=os.path.dirname(os.path.abspath(__file__))
    proc = subprocess.run(['./backgroundjobs/ci.sh'],stdout=subprocess.PIPE,cwd=repo_path)
    test_info=Test_info(commit_id=commit_id,commit_message='123',test_exit_code=proc.returncode,log=proc.stdout.decode('utf-8'))
    test_info.save()

    return "exited the worker"    