#!/usr/bin/env bash

#Ask the user for number of clients
read -p 'Enter number of Local clients (1 to 32):' nC 


for ((c=1; c<=nC; c++))
do
echo 'parcicipant' $c &
sudo docker run -d -v /home/ubuntu/data:/home/data \
	                -v /home/ubuntu/fedserver-data/local_model:/home/local_model --env-file config.env --name "client$c" arijitnandi/fedclient $c 

done
echo "DOCKER STAT LOGGING...."
while true; do sudo docker stats --all --no-stream --format "table {{.ID}}\t{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}\t{{.PIDs}}" | cat >> ./`date -u +"localclient_stats.csv"`; sleep 10; done
