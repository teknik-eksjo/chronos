FROM python:3.5

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip install gunicorn

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
RUN chmod +x manage.py
