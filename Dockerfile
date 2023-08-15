FROM nikolaik/python-nodejs:python3.8-nodejs14

WORKDIR /app


## Install packages
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

ADD . /app
RUN ["chmod", "+x", "/app/start.sh"]
ENTRYPOINT ["sh","./start.sh"]

## Run the application on the port 8080
# EXPOSE 8000