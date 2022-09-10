FROM python:3.6

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY requirements.txt .

# install dependencies
RUN pip install  -r requirements.txt

COPY . .

# run the command
ENTRYPOINT ["python", "run-client.py"]
