#!/usr/bin/env bash

#Ask the user for number of clients
read -p 'Enter number of Local clients (1 to 32):' nC 


for ((c=1; c<=nC; c++))
do
echo 'parcicipant' $c &
sudo docker run -d -v /home/ubuntu/data:/home/data \
	                -v /home/ubuntu/fedserver-data/local_model:/home/local_model --env-file config.env arijitnandi/fedclient $c 

done
