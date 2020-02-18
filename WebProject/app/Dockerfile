#FROM tiangolo/meinheld-gunicorn-flask:python3.7
#FROM tiangolo/uwsgi-nginx-flask:python3.7
#
#COPY ./app /app
#
#RUN pip install -r requirements.txt

#RUN echo "uwsgi_read_timeout 300s;" > /etc/nginx/conf.d/custom_timeout.conf
#RUN echo "proxy_connect_timeout 600;" > /etc/nginx/conf.d/custom_timeout.conf
#RUN echo "proxy_send_timeout 600;" > /etc/nginx/conf.d/custom_timeout.conf
#RUN echo "proxy_read_timeout 600;" > /etc/nginx/conf.d/custom_timeout.conf
#RUN echo "send_timeout 600;" > /etc/nginx/conf.d/custom_timeout.conf


FROM python:3.7.4-stretch

ADD . /app

WORKDIR /app



RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 8000

CMD ["gunicorn","-t","300","-b", "0.0.0.0:8000", "main:app"]

