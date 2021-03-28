import argparse
import base64
from PIL import Image
import cv2
import io
import numpy as np
from backend.yolo import YOLO
import re

class VideoProc:
    def __init__(self, size = 416, confidence = 0.25, hand_count = 2):
        self.confidence = confidence
        self.size = size
        self.yolo = YOLO("static/models/cross-hands-tiny.cfg", "static/models/cross-hands-tiny.weights", ["hand"])

        self.hand_count = hand_count
        
    def b64_to_image(self, base64_string):
        # altchars = b'+/'
        # base64_string = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', str.encode(base64_string))  # normalize
        # missing_padding = len(base64_string) % 4
        # if missing_padding:
        #     base64_string += b'='* (4 - missing_padding)

        imgdata = base64.decodebytes(base64_string[22:].encode('utf-8'))

        sbuf = io.BytesIO(imgdata)
        image = Image.open(sbuf)

        return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        


        # imgdata = base64.b64decode(base64_string + b'=' * (-len(base64_string) % 4))
        # sbuf.write(base64.b64decode(base64_string))
        # pimg = Image.open(sbuf)
        
        # return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

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

            