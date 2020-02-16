import grpc
import shared.video_frame_pb2 as video_frame_pb2
import shared.video_frame_pb2_grpc as video_frame_pb2_grpc
import numpy as np
import cv2
from PIL import Image
import datetime as dt

SERVER_ADDRESS = '127.0.0.1:50051'
CAMERA_SOURCE = 0
WIDTH, HEIGHT = 280, 280


def infinity_loop(cap):
    while cap.isOpened():
        yield
    print('Camera stream was closed')


def generateRequests():
    print('Accessing camera stream')
    cap = cv2.VideoCapture(CAMERA_SOURCE)
    for _ in infinity_loop(cap):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = cv2.resize(gray, (WIDTH, HEIGHT))
        pil_image = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(pil_image).convert('L')
        numpy_array = np.array(pil_image, 'uint8')
        yield video_frame_pb2.FrameRequest(
            img=numpy_array.tobytes(),
            width=WIDTH,
            height=HEIGHT,
            fps=30,
            isColor=False)


def run():
    channel = grpc.insecure_channel(SERVER_ADDRESS)
    stub = video_frame_pb2_grpc.VideoFrameStub(channel)
    for response in stub.Send(generateRequests()):
        print(f"{dt.datetime.now()}: {str(response.reply)}")


if __name__ == '__main__':
    run()
