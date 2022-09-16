FROM python

# set a directory for the app
WORKDIR /home/gp/arin-app

# copy all the files to the container
COPY requirements.txt .

# install dependencies
RUN pip install  -r requirements.txt

COPY . .

# run the command
ENTRYPOINT ["python", "run-client.py"]
