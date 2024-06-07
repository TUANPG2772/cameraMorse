import cv2

class Webcam2rgb:
    def __init__(self):
        self.cap = None
        self.running = False

    def start(self, callback, cameraNumber=0):
        self.cap = cv2.VideoCapture(cameraNumber, cv2.CAP_V4L2)
        if not self.cap.isOpened():
            print("Error: Could not open video capture")
            return

        # Điều chỉnh các tham số như độ phân giải, FPS, và codec
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 680)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 680)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

        self.running = True
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            # Chuyển frame sang callback
            callback(ret, frame)

    def stop(self):
        self.running = False
        if self.cap is not None:
            self.cap.release()
