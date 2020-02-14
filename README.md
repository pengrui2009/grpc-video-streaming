# video-streaming-grpc
video streaming with grpc

change to virtualenv

pip install grpcio

pip install grpcio-tools

pip install opencv-python

pip install scikit-video

from root folder:
python -m grpc_tools.protoc -I./src/protos --python_out=./src/ --grpc_python_out=./src/ ./src/protos/image.proto