FROM python:3.9.15-slim-buster

WORKDIR /app
COPY . /app/
RUN pip install --upgrade pip --no-cache-dir

RUN pip install -r /app/requirment.txt --no-cache-dir
# RUN apt-get install -y ffmpeg
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg

# CMD ["python3","manage.py","runserver","0.0.0.0:8000"]

CMD ["gunicorn","awsvideoupload.wsgi:application","--bind", "0.0.0.0:8000"]
