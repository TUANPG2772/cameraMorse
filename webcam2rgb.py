import os
import fcntl
import mmap
import struct
import threading

class Webcam2rgb:
    def __init__(self):
        self.device = "/dev/video0"
        self.fmt = struct.pack("HH", 640, 480)  # Set the resolution here
        self.fmt += b"YUYV"
        self.fd = os.open(self.device, os.O_RDWR)
        self.map = mmap.mmap(self.fd, os.fstat(self.fd).st_size, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE)

    def start(self, callback, width=None, height=None, fps=None):
        self.callback = callback
        self.width = width
        self.height = height
        self.fps = fps
        self.running = True
        self.thread = threading.Thread(target=self._read_frames)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def _read_frames(self):
        while self.running:
            try:
                fcntl.ioctl(self.fd, 0x80685600, self.fmt)  # VIDIOC_S_FMT
                frame = self.map[:640*480*2]
                self.map.seek(0)
                frame = np.frombuffer(frame, dtype=np.uint8)
                frame = frame.reshape((480, 640, 2))[:, :, 0]  # Extract Y channel
                self.callback(True, frame)
            except Exception as e:
                print("Error:", e)
                self.callback(False, None)

    def cameraFs(self):
        return self.fps
