# video-streaming-grpc

## Prerequisites
1. Installed Python Python 3.7.6 +
1. Camera connected to computer

## Start project without docker
1. If on linux:
```bash
sudo apt-get update
sudo apt-get install -y libgtk2.0-dev
```
1. Install required PIP packages from requirments.txt in root folder
```bash
pip install -r requirments.txt
```
1. Run server
```bash
python ./src/server/server.py
```
1. Run client
```bash
python ./src/client/client.py
```

## Run with docker
1. Run docker-compose
```bash
docker-compose -f "src\docker-compose.yml" up -d --build
```
1. Run client
```bash
python ./src/client/client.py
```


## Generate new proto files example
1. Run from root folder
```bash
python -m grpc_tools.protoc -I./src/protos --python_out=./src/ --grpc_python_out=./src/ ./src/protos/video_frame.proto
```