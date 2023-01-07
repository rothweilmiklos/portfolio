FROM python:3
ENV PYTHONBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
#CMD python manage.py runserver 0.0.0.0:8000
CMD gunicorn --bind 0.0.0.0:8004 -w 3 random_apis.wsgi