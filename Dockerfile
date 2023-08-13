FROM python:3.10
WORKDIR /usr/src/app

## Install packages
COPY requirements.txt ./
RUN pip install -r requirements.txt

## Run the application on the port 8080
# EXPOSE 8000