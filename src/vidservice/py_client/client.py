import cv2
from vidservice.proto_definations import (video_streaming_pb2_grpc, video_streaming_pb2)
import logging
import grpc
import numpy as np
import base64

def create_video_request(uuid:str):
    return video_streaming_pb2.VideoMetaData(value=uuid, html=0)

def view_video(stub:video_streaming_pb2_grpc.VideoStreamerStub):
    frames = stub.getVideoStream(request=create_video_request("1-sec"))
    count = 0
    cv2.namedWindow("view-video-stream")
    for frame in frames:
        b64decoded = base64.b64decode(frame.b64image)
        imgarr = np.frombuffer(b64decoded, dtype=np.uint8).reshape(frame.width, frame.height, -1)

        logging.info("Recieved video frame {count}")
        cv2.imshow("view-video-stream", imgarr)
        
        client_key_press = cv2.waitKey(1) & 0xFF
        # end video stream by escape key
        if client_key_press == 27:
            break

        count+=1
    if count == 0:
        logging.info("No frames recieved!")
    cv2.destroyAllWindows()
    
def run():
    logging.info("Starting client...")
    options = [('grpc.max_send_message_length', 512 * 1024 * 1024), ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
    with grpc.insecure_channel("0.0.0.0:50051", options=options) as channel:
        stub = video_streaming_pb2_grpc.VideoStreamerStub(channel)
        view_video(stub)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run()