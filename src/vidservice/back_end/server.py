import logging
from pathlib import Path
import threading
import grpc
import enum
from concurrent.futures import ThreadPoolExecutor
from typing import MutableMapping, List, Optional
import logging
import numpy as np
import vidservice.back_end.streamer.videostreamer as videostreamer
import vidservice.back_end.streamer.filestreamer as filestreamer
import vidservice.back_end.streamer.camerastreamer as camerastreamer
from vidservice.proto_definations import video_streaming_pb2_grpc, video_streaming_pb2


class StreamType(enum.IntEnum):
    FileStreamer = 0
    CameraStreamer = 1
class VideoServer(video_streaming_pb2_grpc.VideoStreamerServicer):
    def __init__(self) -> None:
        self.run = True
        self.streamtype = StreamType.CameraStreamer
        self.streamer_apis = List[videostreamer.VideoStreamer]
        
        # prepare video path based on uuid
        base_path = Path(__file__).parent.absolute().parents[1]
        video_file = "1-sec.mp4"
        video_uuid_path = base_path / "videos" / video_file
        print('video_uuid_path:{}'.format(video_uuid_path))
        # Get request
        should_encode_for_html = False
        
        self.streamer_apis = [
            filestreamer.FileStreamer(video_uuid_path, html=should_encode_for_html),
            camerastreamer.CameraStreamer(0, html=should_encode_for_html)
        ]

    def create_frame(self, frame: np.ndarray, shape):
        return video_streaming_pb2.VideoFrames(
            b64image=frame, width=shape[0], height=shape[1]
        )

    def create_server_signal(self, signal: int):
        return video_streaming_pb2.ServerStreamSignal(signal=signal)

    def controlStream(self, request, context):
        # signal: bool = True 
        if request.signal == 1 :
            signal = True
        else :
            signal = False
        self.run = signal

        if request.stream == 0 :
            self.streamtype = StreamType.FileStreamer
        elif request.stream == 1 :
            self.streamtype = StreamType.CameraStreamer
        else :
            raise ValueError("Invalid stream type {request.stream}")

        if signal:
            logging.info("Signal to START stream in server is AWAITING.")
            return self.create_server_signal(1)
        else:
            logging.info("Signal to END stream in server is AWAITING.")
            return self.create_server_signal(0)

    def getVideoStream(self, request, context):
        # # prepare video path based on uuid
        # base_path = Path(__file__).parent.absolute().parents[1]
        # video_file = request.value + ".mp4"
        # video_uuid_path = base_path / "videos" / video_file
        # print('video_uuid_path:{}'.format(video_uuid_path))
        # # Get request
        # should_encode_for_html = request.html == 1
        # self.streamer_api = filestreamer.VideoStreamer(
        #     video_uuid_path, html=should_encode_for_html
        # )

        if hasattr(self, "run"):
            if not self.run:
                logging.info("Signal to END stream in server is RECIEVED.")
                return
            else:
                self.streamer_apis[self.streamtype].init_video()
                logging.info("Signal to START stream in server is RECIEVED.")
                if (self.streamtype == StreamType.FileStreamer):    
                    frames = self.streamer_apis[self.streamtype].send_frame()
                    # Yield response
                    for frame, shape, status in frames:
                        if not status:
                            break
                        yield self.create_frame(frame, shape)
                elif self.streamtype == StreamType.CameraStreamer :
                    while True :
                        frames = self.streamer_apis[self.streamtype].send_frame()
                        # Yield response
                        for frame, shape, status in frames:
                            if not status:
                                break
                            yield self.create_frame(frame, shape)

                logging.info("All frames have been read, releasing video resources now....")
                self.streamer_apis[self.streamtype].release_video_resources()
                self.run = False 

def serve(address: str) -> None:
    server = grpc.server(ThreadPoolExecutor(10))
    vid_serve = VideoServer()
    video_streaming_pb2_grpc.add_VideoStreamerServicer_to_server(vid_serve, server)
    server.add_insecure_port(address)
    server.start()
    logging.info("Server serving at %s", address)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve("0.0.0.0:50051")
