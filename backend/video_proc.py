import argparse
import base64
from PIL import Image
import cv2
from io import StringIO
import numpy as np
from backend.yolo import YOLO

class VideoProc:
    def __init__(self, size = 416, confidence = 0.25, hand_count = 2):
        self.confidence = confidence
        self.size = size
        self.yolo = YOLO("static/models/cross-hands-tiny.cfg", "static/models/cross-hands-tiny.weights", ["hand"])

        self.hand_count = hand_count
        
    def b64_to_image(self,base64_string):
        sbuf = StringIO()
        sbuf.write(base64.b64decode(base64_string))
        pimg = Image.open(sbuf)
        return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

    def process_image(self, frame):
        frame = self.b64_to_image(frame)
        width, height, inference_time, results = self.yolo.inference(frame)

        results.sort(key=lambda x: x[2])

        # how many hands should be shown
        hand_count = len(results)
        hand_count = self.hand_count

        # display hands

        for detection in results[:hand_count]:
            id, name, confidence, x, y, w, h = detection
            return(x,y,w,h)

            