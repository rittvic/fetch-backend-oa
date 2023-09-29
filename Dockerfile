FROM python:3.10-slim-buster

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["flask","--app","server","run","--port","8000","--host","0.0.0.0"]