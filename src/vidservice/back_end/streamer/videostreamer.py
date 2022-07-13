"""
    Core functionality to stream videos.
    Use send_frames as this is a generator that will yield a base64 encoded frame.
    @author: Rohan Deshpande
"""
import logging
import queue
import logging
import cv2 as cv
import numpy as np
import base64
import time
from threading import Thread
from pathlib import Path

class VideoStreamer(object):
    def __init__(self) -> None:

        self.video=None
        self.activate = False
        self.html = None

    def init_video(self):
        """
            Init video threads, and open-cv stuff.
        """
        raise NotImplementedError('VideoStreamer is a base class and should NEVER be instantiated.')
    
    def start_video(self):
        """
            Start threads
        """
        raise NotImplementedError('VideoStreamer is a base class and should NEVER be instantiated.')
        
    
    def release_video_resources(self):
        """
            Join threads, and release resources
        """
        raise NotImplementedError('VideoStreamer is a base class and should NEVER be instantiated.')

    def read_frame(self):
        """
            Put all frames in the queue.
        """
        raise NotImplementedError('VideoStreamer is a base class and should NEVER be instantiated.')
    
    def preprocess_frame(self, frame: np.ndarray):
        """
            Preprocess frames before sending them to client.
        """
        raise NotImplementedError('VideoStreamer is a base class and should NEVER be instantiated.')

    def send_frame(self):
        """
            Send frames to client at a constant rate.
        """
        raise NotImplementedError('VideoStreamer is a base class and should NEVER be instantiated.')