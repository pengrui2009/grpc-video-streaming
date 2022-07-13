import time
from typing import MutableMapping, List, Optional

from vidservice.back_end.streamer.filestreamer import FileStreamer
from vidservice.back_end.streamer.camerastreamer import CameraStreamer
from vidservice.proto_definations.video_streaming_pb2_grpc import VideoStreamer

if __name__ == '__main__':
    # players = List[VideoStreamer]
    stream = CameraStreamer(0, False)
    stream.init_video()

    # stream.start_video()
    for i in range(1000):
        frames = stream.send_frame()
        for frame, shape, status in frames:
            print('shape:{} status:{}'.format(shape, status))
        print('+++++++++++++++++++')
        # stream.read_frame()
        time.sleep(1)

    stream.release_video_resources()