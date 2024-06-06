import cv2
import threading
import numpy as np
# thay roi
class Webcam2rgb:
    def __init__(self):
        self.device = 0  # Sử dụng camera mặc định
        self.width = 640
        self.height = 480
        self.cap = cv2.VideoCapture(self.device, cv2.CAP_V4L2)
        if not self.cap.isOpened():
            raise Exception("Could not open video device")

        # Đặt độ phân giải cho camera
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'YUYV'))

    def start(self, callback, width=None, height=None, fps=None):
        self.callback = callback
        self.width = width if width else self.width
        self.height = height if height else self.height
        self.fps = fps
        self.running = True
        self.thread = threading.Thread(target=self._read_frames)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()
        self.cap.release()

    def _read_frames(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Could not read frame")
                self.callback(False, None, None)
                continue

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_YUV2RGB_YUYV)
            self.callback(True, frame_rgb, frame)

    def cameraFs(self):
        return self.cap.get(cv2.CAP_PROP_FPS)
