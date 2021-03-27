import argparse

from yolo import YOLO

class VideoProc:
    def init(self, size = 416, confidence = 0.25, hand_count = 2):
        self.confidence = confidence
        self.size = size
        self.yolo = YOLO("models/cross-hands-tiny.cfg", "models/cross-hands-tiny.weights", ["hand"])

        self.hand_count = hand_count

    def process_image(self, frame):
        width, height, inference_time, results = self.yolo.inference(frame)

        results.sort(key=lambda x: x[2])

        # how many hands should be shown
        hand_count = len(results)
        hand_count = self.hand_count

        # display hands
        hands = []

        for detection in results[:hand_count]:
            id, name, confidence, x, y, w, h = detection

            hands.append(x, y, w, h, confidence)
        
        return hands
            