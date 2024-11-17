import cv2
from datetime import datetime
import os

class VideoWriter:
    def __init__(self, output_dir, fps=30):
        self.output_dir = output_dir
        self.fps = fps
        self.writers = {}  # Dictionary to manage active video writers per track ID

    def start_writing(self, track_id, frame):
        if track_id not in self.writers:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{self.output_dir}/{track_id}_{timestamp}.mp4"
            height, width, _ = frame.shape
            writer = cv2.VideoWriter(
                filename, cv2.VideoWriter_fourcc(*"mp4v"), self.fps, (width, height)
            )
            self.writers[track_id] = writer
            return filename
        return None

    def write_frame(self, track_id, frame):
        if track_id in self.writers:
            self.writers[track_id].write(frame)

    def stop_writing(self, track_id):
        if track_id in self.writers:
            self.writers[track_id].release()
            del self.writers[track_id]

    def stop_all(self):
        for writer in self.writers.values():
            writer.release()
        self.writers.clear()
