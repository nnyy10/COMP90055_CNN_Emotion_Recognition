#FROM tiangolo/meinheld-gunicorn-flask:python3.7
FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ./app /app

#RUN apt update && apt upgrade -y
#ENV

RUN pip install -r requirements.txt

#RUN echo "uwsgi_read_timeout 300s;" > /etc/nginx/conf.d/custom_timeout.conf


#FROM python:3.7.4-stretch
#
#WORKDIR /app
#
#ADD . /app
#
#RUN pip install -r requirements.txt
#
#EXPOSE 5000
#
#CMD ["python3","main.py"]

