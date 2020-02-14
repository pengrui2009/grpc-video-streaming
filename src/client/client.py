import grpc
import cv2
import image_pb2
import image_pb2_grpc
import skvideo.io

URL = "run_terraform.mkv"


def run():
    channel = grpc.insecure_channel('127.0.0.1:50051')
    stub = image_pb2_grpc.ImageTestStub(channel)
    for response in stub.Analyse( generateRequests() ):
      print(str(response.reply))

def infinity():
    while True:
        yield

def generateRequests():
   cap = cv2.VideoCapture(0)
   for _ in infinity():
       # Capture frame-by-frame
       ret, frame = cap.read()
       # Our operations on the frame come here
       gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
       # Display the resulting frame cv2.imshow('frame', gray)
       frame = bytes(frame)
       yield image_pb2.MsgRequest(img=frame)


if __name__ == '__main__':
  run()
