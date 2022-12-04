FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
CMD gunicorn --bind 0.0.0.0:8003 -w 3 middle_earth_inventory.wsgi