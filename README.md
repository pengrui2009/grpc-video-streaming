# video-streaming-grpc
video streaming with grpc

change to virtualenv

pip install grpcio

pip install grpcio-tools

from root folder:
python -m grpc_tools.protoc -I./src/protos --python_out=./src/ --grpc_python_out=./src/ ./src/protos/image.proto