FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip --no-cache-dir
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
#CMD python manage.py runserver
CMD gunicorn --bind 0.0.0.0:8002 -w 3 middle_earth_items.wsgi