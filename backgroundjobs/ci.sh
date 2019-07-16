#!/bin/bash

# change the pwd to home
#cd 

# change the pwd to repo directory
#cd $1

# checkout to recent push's commit using commit_id
#git checkout $2

# find the direcotry which contains docker-compose.yml and change the pwd to it
cd "$(find -iname "docker-compose.yml" -printf '%h' -quit)"

# build the containers from the docker-compose
timeout -k 10 10 sudo docker-compose up --build

if [ $?==124 ]
then
    echo "timed-out"
    sudo docker-compose down
    exit 2
fi

# sudo docker-compose up --build

## search for the result of test cases
# if OK i.e., test passed else failed
sudo docker-compose logs|pcregrep -M 'Ran . (test|tests) in (0|[1-9]\d*)(\.\d+)?s(\n).*(\n).*OK'

if [ !$? ]
then 
    echo "passed"
    sudo docker-compose down
    exit 0
else 
    echo "failed"
    sudo docker-compose down
    exit 1
fi


# send the data exit codes and the logs files to the database