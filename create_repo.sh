#! ~/bin/bash
# $1: Username and $2: Repo name
cd users
git init --bare $2
git clone git@<ip_add>:$1/$2.git

bash -c 'cat >  $2.git/hooks <<EOF
#!/bin/bash

while read oldrev newrev ref
do
    unset $(git rev-parse --local-env-vars)
    cd ~/$1/$2
    git pull
done

EOF'

