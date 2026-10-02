import cv2
from mjpeg_streamer import MjpegServer, Stream

class MJPEG_Handler:
    def __init__(self, camera):
        self.cap = cv2.VideoCapture(0)
        self.stream = Stream("my_camera", size=(640, 480), quality=50, fps=30)
        self.server = MjpegServer("localhost", 8080)
        self.server.add_stream(self.stream)
        self.server.start()

    def send_stream(self):
        _, frame = self.cap.read()
        cv2.imshow(self.stream.name, frame)            

        self.stream.set_frame(frame)

        print(round(self.stream.get_bandwidth() / 1024, 2), "KB/s", end="\r")

    '''server.stop()
    cap.release()
    cv2.destroyAllWindows()'''