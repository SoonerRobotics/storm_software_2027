import cv2
import mjpeg_test
import struct, numpy as np
import sys
from multiprocessing import shared_memory

cap = cv2.VideoCapture(1)
_, frame = cap.read()
shm = shared_memory.SharedMemory(name = "Frame", create=True, size=sys.getsizeof(frame))
buff = shm.buf
mjpeg = mjpeg_test.MJPEG_Handler()
while True:
    _, frame = cap.read()
    buff = frame
    mjpeg.send_stream(buff)
    #cv2.imshow("image", buff)
    if cv2.waitKey(1) == ord("q"):
        shm.close()
        shm.unlink()
        break
