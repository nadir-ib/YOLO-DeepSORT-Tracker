import cv2
from ultralytics import YOLO

class YOLODetector:
    def __init__(self, config):
        self.model = YOLO(config['yolo']['model_path'], verbose=False)
        self.classes = self.model.names
        self.confidence_threshold = config['yolo']['confidence_threshold']

    def detect(self, frame):
        results = self.model(frame, verbose=False)
        detections = []

        for result in results:
            boxes = result.boxes
            for r in result.boxes.data.tolist():
                if len(r) < 6:
                    continue

                x1, y1, x2, y2 = r[:4]
                w, h = x2 - x1, y2 - y1
                coordinates = list((int(x1), int(y1), int(w), int(h)))
                conf = r[4]
                cls_id = int(r[5])
                cls = self.classes[cls_id]

                if cls in ["person", "cat", "dog"] and conf > self.confidence_threshold:
                    detections.append((coordinates, conf, cls))

        return detections
