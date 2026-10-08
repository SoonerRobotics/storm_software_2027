import cv2
from mjpeg_streamer import MjpegServer, Stream
from multiprocessing import shared_memory

class MJPEG_Handler:
    def __init__(self):
        #self.frame = frame
        self.stream = Stream("my_camera", size=(640, 480), quality=50, fps=30)
        self.server = MjpegServer("192.168.1.128", 8080)
        self.server.add_stream(self.stream)
        self.server.start()

    def send_stream(self, frame):
        self.frame = frame
        cv2.imshow(self.stream.name, self.frame)            

        self.stream.set_frame(self.frame)

        #(round(self.stream.get_bandwidth() / 1024, 2), "KB/s", end="\r")

#shm = shared_memory.SharedMemory(name = "Frame", create=False)
#buf = shm.buf

#mjpeg = MJPEG_Handler(buf)
