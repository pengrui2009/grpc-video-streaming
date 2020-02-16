import grpc
import shared.video_frame_pb2 as video_frame_pb2
import shared.video_frame_pb2_grpc as video_frame_pb2_grpc
import numpy as np
import cv2
from PIL import Image


def infinity_loop(cap):
    while cap.isOpened():
        yield
    print('Camera stream was closed')


def generateRequests():
    print('Accessing camera stream')
    cap = cv2.VideoCapture(0)
    for _ in infinity_loop(cap):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        width_d, height_d = 280, 280  # Declare your own width and height
        face = cv2.resize(gray, (width_d, height_d))
        pil_image = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(pil_image).convert('L')
        numpy_array = np.array(pil_image, 'uint8')
        print(numpy_array)
        print(type(numpy_array))
        yield video_frame_pb2.FrameRequest(img=numpy_array.tobytes())


def run():
    channel = grpc.insecure_channel('127.0.0.1:50051')
    stub = video_frame_pb2_grpc.VideoFrameStub(channel)
    for response in stub.Send(generateRequests()):
        print(str(response.reply))


if __name__ == '__main__':
    run()
