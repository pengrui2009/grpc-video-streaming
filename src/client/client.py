import grpc
import video_frame_pb2
import video_frame_pb2_grpc
import numpy as np
import cv2
import datetime as dt

SERVER_ADDRESS = '127.0.0.1:50051'
CAMERA_SOURCE = 0


def infinity_loop(cap):
    while cap.isOpened():
        yield
    print('Camera stream was closed')


def generateRequests():
    print('Accessing camera stream')
    cap = cv2.VideoCapture(CAMERA_SOURCE)
    width, height = None, None
    for _ in infinity_loop(cap):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if width is None:
            height, width = gray.shape
        yield video_frame_pb2.FrameRequest(
            img=gray.tobytes(),
            width=width,
            height=height,
            fps=30,
            isColor=False)


def run():
    channel = grpc.insecure_channel(SERVER_ADDRESS)
    stub = video_frame_pb2_grpc.VideoFrameStub(channel)
    for response in stub.Send(generateRequests()):
        print(f"{dt.datetime.now()}: {str(response.reply)}")


if __name__ == '__main__':
    run()
