#usb to hdmi v2 "многопоточность"

import cv2
import numpy as np
import threading
import time

class CameraReader(threading.Thread):
    def __init__(self, src=0, desired_size=(1280, 720)):
        threading.Thread.__init__(self)
        self.src = src
        self.desired_size = desired_size
        self.frame = None
        self.running = True
        self.connected = False

    def run(self):
        while self.running:
            try:
                self.cap = cv2.VideoCapture(self.src)
                if self.cap.isOpened():
                    self.connected = True
                    while self.running:
                        ret, frame = self.cap.read()
                        if ret:
                            self.frame = cv2.resize(frame, self.desired_size)
                        else:
                            break
                else:
                    time.sleep(1)  
            finally:
                self.cap.release()

    def get_frame(self):
        return self.frame

    def is_connected(self):
        return self.connected

    def stop(self):
        self.running = False
        if self.cap.isOpened():
            self.cap.release()

def show_message(window_name, msg, desired_size):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    line_type = 2
    text_size, _ = cv2.getTextSize(msg, font, font_scale, line_type)
    text_x = (desired_size[0] - text_size[0]) // 2
    text_y = (desired_size[1] + text_size[1]) // 2

    img = np.zeros((desired_size[1], desired_size[0], 3), dtype=np.uint8)
    cv2.putText(img, msg, (text_x, text_y), font, font_scale, (255, 255, 255), line_type)
    cv2.imshow(window_name, img)
    cv2.waitKey(1)

# задаем размер
desired_size = (1280, 720)
camera_reader = CameraReader(desired_size=desired_size)
camera_reader.start()

cv2.namedWindow("Camera", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Camera", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

try:
    while not camera_reader.is_connected():
        show_message("Camera", "Connecting to camera...", desired_size)
        time.sleep(1)

    while True:
        frame = camera_reader.get_frame()
        if frame is not None:
            cv2.imshow('Camera', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    camera_reader.stop()
    cv2.destroyAllWindows()
