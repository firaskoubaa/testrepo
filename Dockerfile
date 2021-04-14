FROM python:3.9.1

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt    

RUN apt update && apt install -y nginx 

RUN cp nginx_config /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/nginx_config /etc/nginx/sites-enabled/nginx_config

EXPOSE 5000

CMD service nginx start && gunicorn -c gunicorn_config.py mywebapp.wsgi



# Commands:
# sudo docker build -t djwebapp:1.1 .
# sudo docker run -it -v $(pwd):/app:ro -d -p 7001:5000  djwebapp:1.1