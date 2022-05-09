FROM python:3.7

COPY . /home
WORKDIR /home

RUN apt-get update && apt-get -y install \
    build-essential libpcre3 libpcre3-dev zlib1g zlib1g-dev libssl-dev wget
RUN apt-get -y  install build-essential 
RUN apt-get -y install libglu1-mesa

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "app.py"]
