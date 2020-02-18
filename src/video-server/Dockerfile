FROM python:3.8.1-slim-buster

LABEL Name=grpc-video-serve Version=0.0.1
EXPOSE 50051

WORKDIR /src
ADD /video-server /src

RUN apt-get update
RUN apt-get install -y libgtk2.0-dev

RUN python3 -m pip install -r requirements.txt
CMD ["python3", "./server.py"]