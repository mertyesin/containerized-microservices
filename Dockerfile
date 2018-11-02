FROM python:3.5.2
MAINTAINER Mustafa Mert Yeşin "mertyesin89@gmail.com"
RUN apt-get update -y
RUN apt-get install python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]