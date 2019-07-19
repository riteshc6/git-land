#!/bin/bash
cd $2
git log -n 1 --pretty=format:%s%b -- ./$1