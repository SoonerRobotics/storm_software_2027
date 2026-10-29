import cv2
from mjpeg_streamer import MjpegServer, Stream
from multiprocessing import shared_memory

class MJPEG_Handler:
    def __init__(self):
        #self.frame = frame
        self.stream = Stream("my_camera", size=(320, 240), quality=40, fps=24)
        self.server = MjpegServer("localhost", 8000)
        self.server.add_stream(self.stream)
        self.server.start()

    def send_stream(self, frame):
        self.frame = frame
        #cv2.imshow(self.stream.name, self.frame)

        self.stream.set_frame(self.frame)

        print(round(self.stream.get_bandwidth() / 1024, 2), "KB/s", end="\r")

#shm = shared_memory.SharedMemory(name = "Frame", create=False)
#buf = shm.buf

#mjpeg = MJPEG_Handler(buf)
