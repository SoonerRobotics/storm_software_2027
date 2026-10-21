import cv2
import mjpeg_test
import apriltag
import struct, numpy as np
import sys
from multiprocessing import shared_memory
import http.server
import socketserver

cap = cv2.VideoCapture(0)
_, frame = cap.read()
shm = shared_memory.SharedMemory(name = "Frame", create=True, size=sys.getsizeof(frame))
buff = shm.buf
mjpeg = mjpeg_test.MJPEG_Handler()
a_t = apriltag.AprilTagProcessing()

'''PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()'''

try:
	while True:
		_, frame = cap.read()
		buff = frame
		mjpeg.send_stream(buff)
		a_t.pose_estimation(buff)
	    #cv2.imshow("image", buff)
		if cv2.waitKey(1) == ord("q"):
			break
except:
	print("exit")
finally:
	shm.close()
	shm.unlink()
