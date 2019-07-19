#! /bin/bash
cd $2
git log -1 --format=%cr"|"%s%b ./$1
