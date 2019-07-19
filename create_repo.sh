#! /bin/bash
# $1: Username and $2: Repo name
cd
cd $1
git init --bare $2.git
git clone gitlab@13.233.153.31:$1/$2.git
path=$(pwd)/$2
cat >  $2.git/hooks/post-receive <<EOL
#!/bin/bash

while read oldrev newrev ref
do
    unset \$(git rev-parse --local-env-vars)
    cd ~/$1/$2
    git pull > /dev/null 2>&1
    message=\$(git log -1 --pretty=format:'%s%b' $newrev)
    cd ~/git-land
    source venv/bin/activate
    export DJANGO_SETTINGS_MODULE=mysite.settings
    python -c "import django; django.setup(); from backgroundjobs.views import call_celery; call_celery('$path', '\$newrev','\$message')"
done

EOL
chmod +x $2.git/hooks/post-receive
