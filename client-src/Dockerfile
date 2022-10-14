FROM python:latest

#set a directory for the app
WORKDIR /home/app

RUN mkdir -p /home/data
RUN mkdir -p /home/global_model
RUN mkdir -p /home/local_model

# copy all the files to the container
COPY requirements.txt .

# install dependencies
RUN pip3 install  -r requirements.txt

COPY . .

# run the command
ENTRYPOINT ["python3", "run-client.py"]
