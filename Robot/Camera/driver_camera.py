import cv2
import mjpeg_streaming
import apriltag
import sys
from multiprocessing import shared_memory
from websockets.sync.client import connect
import asyncio


class Camera():
	def __init__(self):
		self.cap = cv2.VideoCapture(0)
		_, self.frame = self.cap.read()
		self.shm = shared_memory.SharedMemory(name = "Frame", create=True, size=sys.getsizeof(self.frame))
		self.buff = self.shm.buf
		self.mjpeg = mjpeg_streaming.MJPEG_Handler()
		self.a_t = apriltag.AprilTagProcessing()

	async def connect_camera(self):
		try:
			async with connect("ws://192.168.1.128:8765", ping_interval=None) as websocket:
				while True:
					_, self.frame = self.cap.read()
					self.buff = self.frame
					self.mjpeg.send_stream(self.buff)
					#a_t.pose_estimation(buff)
					await websocket.send("Bandwidth: " + str(self.mjpeg.bw) +"KB/s")
		except Exception as exc:
			print(f"Client error: {exc!r}")
		finally:
			self.shm.close()
			self.shm.unlink()
   
	def run_camera(self):
		asyncio.run(self.connect_camera())
