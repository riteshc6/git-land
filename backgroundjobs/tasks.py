from __future__ import absolute_import,unicode_literals
from celery.decorators import task
import os
import subprocess
from git_land.models import Test_info, Repository
# from .models import Test_info

@task(name='unit-testing')
def run_the_container(repo_path,commit_id):

    repo=Repository.objects.get(repo_path=repo_path)
    # repo_path=os.path.dirname(os.path.abspath(__file__))
    proc = subprocess.run(['/home/gitlab/git-land/backgroundjobs/ci.sh', commit_id],stdout=subprocess.PIPE,cwd=repo_path)
    test_info=Test_info(commit_id=commit_id,commit_message='123',repo=repo,test_exit_code=proc.returncode,log=proc.stdout.decode('utf-8'))
    test_info.save()

    # return {'reslt':test_info.id,'repo_id':repo.id}
    return {'result':test_info.id,'repo_id':repo.id}    
