import grpc
import image_pb2
import image_pb2_grpc
import numpy as np
import cv2



def run():
    channel = grpc.insecure_channel('127.0.0.1:50051')
    stub = image_pb2_grpc.ImageTestStub(channel)
    for response in stub.Analyse(generateRequests()):
      print(str(response.reply))


def infinity(cap):
    while cap.isOpened():
        print('cap is open')
        yield
    print('cap is not open anymore')


def generateRequests():
   cap = cv2.VideoCapture(0)
   for _ in infinity(cap):
        ret, frame = cap.read()
        # pil_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # pil_image = Image.fromarray(pil_image).convert('L')
        # numpy_array = np.array(pil_image, 'uint8').tobytes()
        # print(len(numpy_array))
        cv2.imshow('test2',frame)
        yield image_pb2.MsgRequest(img=bytes(frame))


if __name__ == '__main__':
  run()