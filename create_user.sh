#! /bin/bash
# $1: ssh_key, $2: username  are arguments to run this script
cd ~/.ssh
echo $1 >> id_$2.pub
cat id_$2.pub >> authorized_keys
cd ..
mkdir $2
