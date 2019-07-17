#! /bin/bash
# $1: Username and $2: Repo name
cd ~/
cd users/$1
git init --bare $2.git
git clone git@13.233.153.31:$1/$2.git

bash -c 'cat >  $2.git/hooks/post-receive <<EOF
#!/bin/bash

while read oldrev newrev ref
do
    unset $(git rev-parse --local-env-vars)
    cd ~/$1/$2
    git pull
done

EOF'

