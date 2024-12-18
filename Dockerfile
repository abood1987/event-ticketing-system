FROM python:3.9-slim

WORKDIR /web_app
COPY . /web_app

RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]
