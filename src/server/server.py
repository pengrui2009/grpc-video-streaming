import image_pb2
import image_pb2_grpc
from concurrent import futures
import grpc
import time
import cv2
import numpy as np

_ONE_DAY_IN_SECONDS = 0


class Server(image_pb2_grpc.ImageTestServicer):

    def Analyse(self, request_iterator, context):
        for req in request_iterator:
          print('rec')
          frame = np.frombuffer(req.img,dtype=np.uint8)
          width_d, height_d = 280, 280  # Declare your own width and height
          frame=frame.reshape(width_d, height_d)
          print(frame.shape)
          cv2.imshow('res',frame)
          yield image_pb2.MsgReply(reply=1)


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  image_pb2_grpc.add_ImageTestServicer_to_server(Server(), server)
  server.add_insecure_port('[::]:50051')
  print('Server starting')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)


if __name__ == '__main__':
  serve()
