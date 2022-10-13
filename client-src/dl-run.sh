
sudo docker run -v /home/ubuntu/data:/home/data \
	                -v /home/ubuntu/fedserver-data/local_model:/home/local_model --env-file config.env arijitnandi/fedclient $1
