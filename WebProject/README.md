# WebProject
## Flask-Guicorn-Docker Description

Python flask web application running on Gunicorn and dockerized in a single container and deployed on a unbuntu server provided by Unimelb Research Cloud.

Gunicorn is a Python WSGI HTTP Server for UNIX.It's a pre-fork worker model. The Gunicorn server is broadly compatible with various web frameworks, simply implemented, light on server resources, and fairly speedy.

Docker is a tool designed to make it easier to create, deploy, and run applications by using containers.it is possible to get far more apps running on the same old servers and it also makes it very easy to package and ship programs

## how to use

### run flask on Gunicorn

firstly, to run flask application on Gunicorn, we have to install Gunicorn.

In your virtual environment, install Gunicorn by using pip:
`pip install Gunicorn`

To run flask by Gunicorn, enter the directory where main.app is in :

`gunicorn -t 300 -b 0.0.0.0:8000 main:app`

`gunicorn` is the command to run flask bu gunicron.

`-t 300` is to set up the timeout to 300s. This is because it takes time to load our deep learning model. We need to increase the timeout limit before the worker is killed.

`-b 0.0.0.0:8000` is to bind the default ip from 127.0.0.1 to 0.0.0.0 and map the port to 8000.
This allows the flask app to listen to requests from public IP not just locally.

`main:app` is the entry point where the module lies. 

`main` refers to main.py where the flask app is running.

`app` refers to the callable application module where `app = Flask(__name__)` is defined.

now wen can run flask on Gunicorn locally. enter localhost:8000 or 0.0.0.0:8000 to view the webpage.

### Dockerize flask and Gunicorn

to dockerize flask and Gunicorn in a single container, we need to create a docker file named Dockerfile under the directory of our web application

Dockerfile is a file specified by docker that contains a list of instructions.

first the Dockerfile must contain a basic image. 

`FROM python:3.7.4-stretch`

Then add all the files in this directory into an app directory created by docker itself.

`ADD . /app`

Set the working directory to app

`WORKDIR /app`

run install command that all libraries needs to be installed.

`RUN pip install -r requirements.txt
RUN pip install gunicorn`

expose the container to port 8000

`EXPOSE 8000`

define the run command that start the app:

`CMD ["gunicorn","-t","300","-b", "0.0.0.0:8000", "main:app"]`

With the Dokerfile, we'll be able to build the docker image by entering the same directory of our Dockerfile and run the command:

`docker build -t myimage .`

to view the existed docker images:

`docker images`

with out image build, to run the image in a container:

`docker run --name give_name_to_contaienr -d -p 80:8000 myimage`

if you want to see the process and bebug information in terminal then just ignore  `-d`

`-p 80:8000` means map the internal port 8000 where our app runs to external 80 which is the default port used by tcp.

with this container running, go to `localhost` or `0.0.0.0` to view the page.


### run container on Ubuntu

to enter the ubuntu server, ` ssh -I /your/directory/to/flask_app_pk ubuntu@45.113.235.79 
` 
The image is already pushed on the docker hub with a tag of 983358/myimage

In the ubuntu server, to pull the image:

`sudo docker pull 983358/myimage`

then, run the same command:

`sudo docker run --name give_container_a_name -d -p 80:8000 983358/myimage`

After that, the app will be successfully run on Gunicorn in a Ubuntu server.
Go to IP `45.113.235.79` to view the page.
