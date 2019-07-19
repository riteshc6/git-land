#!/bin/bash

# change the pwd to home
#cd 

# change the pwd to repo directory
#cd $1

# checkout to recent push's commit using commit_id
git checkout $1

path_for_testing=$(find -iname "docker-compose.yml" -printf '%h' -quit)
if [ $path_for_testing ]
then
    # find the direcotry which contains docker-compose.yml and change the pwd to it
    cd $path_for_testing
    # build the containers from the docker-compose
    timeout --preserve-status -k 100 100 docker-compose up --build

    exit_code=$?
    echo $exit_code
    if [ $exit_code == 137 ]
    then
        echo "timed-out"
        sudo docker-compose down
	git checkout master > /dev/null 2>&1
        exit 2
    elif [ $exit_code == 0 ]
    then
        echo "passed"
        sudo docker-compose down
	git checkout master > /dev/null 2>&1
        exit 0
    else
        echo "test cases failed"
        sudo docker-compose down
	git checkout master > /dev/null 2>&1
        exit 1
    fi
else
    echo "docker-compose.yml file is not found"
    git checkout master > /dev/null 2>&1
    exit 3
fi
# sudo docker-compose up --build

## search for the result of test cases
# if OK i.e., test passed else failed
# sudo docker-compose logs|pcregrep -M 'Ran . (test|tests) in (0|[1-9]\d*)(\.\d+)?s(\n).*(\n).*OK'



# send the data exit codes and the logs files to the database
