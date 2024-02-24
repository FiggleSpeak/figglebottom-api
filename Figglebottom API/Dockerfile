# Pull the base image with python 3.10 as a runtime
FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONUNBUFFERED True

# Install eSpeak-NG
RUN apt-get update && apt-get install -y espeak-ng

# Install pytorch
RUN python3.10 -m pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

#Copy requirements into container
COPY requirements.txt ./

#Install requirements.txt
RUN python3.10 -m pip install -r requirements.txt

#Copy files over into root directory
COPY . .

# Run the web service on container startup. 
# Use gunicorn webserver with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app



