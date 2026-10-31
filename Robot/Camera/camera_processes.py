import cv2
import mjpeg_test
import apriltag
import struct, numpy as np
import sys
from multiprocessing import shared_memory
import http.server
import socketserver
from websockets.sync.client import connect
import asyncio


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

async def main():
	try:
		with connect("ws://192.168.1.128:8765", ping_interval=None) as websocket:
			while True:
				_, frame = cap.read()
				buff = frame
				mjpeg.send_stream(buff)
				#a_t.pose_estimation(buff)
				websocket.send(str(mjpeg.bw))
	except Exception as exc:
		print(f"Client error: {exc!r}")
	finally:
		shm.close()
		shm.unlink()

asyncio.run(main())