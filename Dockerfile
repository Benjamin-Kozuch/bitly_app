FROM python:3.7-alpine

RUN adduser -D bitly_app

WORKDIR /home/bitly_app

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY bitly_app.py boot.sh config.py ./
RUN chmod +x boot.sh

ENV FLASK_APP bitly_app.py

RUN chown -R bitly_app:bitly_app ./
USER bitly_app

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]