import cv2
import numpy as np
import threading

class Webcam2rgb():
    def start(self, callback, cameraNumber=0, width=None, height=None, fps=None):
        self.callback = callback
        try:
            self.cam = cv2.VideoCapture(cameraNumber, cv2.CAP_V4L2) 
            if not self.cam.isOpened():
                print('opening camera')
                self.cam.open(cameraNumber, cv2.CAP_V4L2)
                
            if width:
                self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            if height:
                self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            if fps:
                self.cam.set(cv2.CAP_PROP_FPS, fps)
            self.running = True
            self.thread = threading.Thread(target=self.calc_BGR)
            self.thread.start()
            self.ret_val = True
        except Exception as e:
            print(f"Error: {e}")
            self.running = False
            self.ret_val = False

    def stop(self):
        self.running = False
        self.thread.join()

    def calc_BGR(self):
        while self.running:
            try:
                self.ret_val = False
                self.ret_val, img = self.cam.read()
                if self.ret_val:
                    h, w, c = img.shape
                    bgr = img[int(h/2), int(w/2)]
                    self.callback(self.ret_val, bgr)
            except Exception as e:
                print(f"Error in calc_BGR: {e}")
                self.running = False

    def cameraFs(self):
        return self.cam.get(cv2.CAP_PROP_FPS)
