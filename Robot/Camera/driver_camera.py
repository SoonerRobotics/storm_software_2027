import cv2
import Camera.mjpeg_streaming as mjpeg_streaming
import Camera.apriltag as apriltag
import sys
from multiprocessing import shared_memory
from websockets.sync.client import connect
import asyncio


class Camera():
	def __init__(self, shm, buf):
		self.shm = shm
		self.buff = buf
		self.mjpeg = mjpeg_streaming.MJPEG_Handler()
		self.a_t = apriltag.AprilTagProcessing()
		self.bw = None
		self.cap = cv2.VideoCapture(0)

	def send_frame(self):
		try:
			_, self.frame = self.cap.read()
			self.buff = self.frame
			self.mjpeg.send_stream(self.buff)
			#a_t.pose_estimation(buff)
			self.bw = "Bandwidth: " + str(self.mjpeg.bw) +"KB/s"
			#print(ws.recv())
		except Exception as exc:
			print(f"Client error: {exc!r}")
			self.close()
			
   
	def close(self):
		self.shm.close()
		self.shm.unlink()
   
