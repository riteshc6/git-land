#! /bin/bash
# $1: Username and $2: Repo name
cd
cd $1
git init --bare $2.git
git clone gitlab@13.233.153.31:$1/$2.git
cat >  $2.git/hooks/post-receive <<EOL
#!/bin/bash

while read oldrev newrev ref
do
    unset \$(git rev-parse --local-env-vars)
    cd ~/$1/$2
    git pull
done

EOL
chmod +x $2.git/hooks/post-receive
