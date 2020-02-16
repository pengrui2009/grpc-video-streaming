import grpc
import shared.video_frame_pb2 as video_frame_pb2
import shared.video_frame_pb2_grpc as video_frame_pb2_grpc
import cv2
import numpy as np
import time
from concurrent import futures
import datetime as dt

_ONE_DAY_IN_SECONDS = 0
MAX_WORKERS_NUMBER = 10


class Server(video_frame_pb2_grpc.VideoFrameServicer):

    def set_parameters_on_first_frame(self, request):
        width_d, height_d = request.width, request.height
        out_stream = cv2.VideoWriter(f"video_{dt.datetime.now()}.avi", cv2.VideoWriter_fourcc(
            *'DIVX'), request.fps, (request.width, request.height), isColor=request.isColor)
        return out_stream, width_d, height_d

    def Send(self, request_iterator, context):
        width, height, fps, isColor, out_stream = None, None, None, None, None
        try:
            for req in request_iterator:
                if out_stream is None:
                    out_stream, width_d, height_d = self.set_parameters_on_first_frame(
                        req)
                    print(f"Variables were set:{width_d}, {height_d}")
                frame = np.frombuffer(req.img, dtype=np.uint8)
                frame = frame.reshape(width_d, height_d)
                out_stream.write(frame)
                print(f"{dt.datetime.now()}: Received frame")
                yield video_frame_pb2.FrameReply(reply=1)
        except Exception as identifier:
            print(f'Exception occured when receiving frames. Ex: {identifier}')
        print(f"{dt.datetime.now()}: Video will be saved")
        if out_stream is not None:
            out_stream.release()
            print(f"{dt.datetime.now()}: Video SAVED")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=MAX_WORKERS_NUMBER))
    video_frame_pb2_grpc.add_VideoFrameServicer_to_server(Server(), server)
    server.add_insecure_port('[::]:50051')
    print(f"{dt.datetime.now()}: Server starting")
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        print(f"{dt.datetime.now()}: Server stopping")
        server.stop(0)


if __name__ == '__main__':
    serve()
