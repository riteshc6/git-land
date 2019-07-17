From python:3.6

WORKDIR /app

COPY . /app

RUN mkdir ~/.ssh
RUN touch authorized_keys

RUN mkdir ~/users

RUN pip3 install -r requirements.txt

RUN pip3 install gunicorn

EXPOSE 80

CMD python manage.py migrate && gunicorn -b 0.0.0.0:80 -w 4 mysite.wsgi:application
