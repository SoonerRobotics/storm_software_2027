import cv2
import Robot.Camera.mjpeg_streaming as mjpeg_streaming
import apriltag
import sys
from multiprocessing import shared_memory
from websockets.sync.client import connect


class Camera():
	def __init__(self):
		self.cap = cv2.VideoCapture(0)
		_, self.frame = self.cap.read()
		self.shm = shared_memory.SharedMemory(name = "Frame", create=True, size=sys.getsizeof(frame))
		self.buff = self.shm.buf
		self.mjpeg = mjpeg_streaming.MJPEG_Handler()
		self.a_t = apriltag.AprilTagProcessing()

	def run_camera(self):
		try:
			with connect("ws://192.168.1.128:8765", ping_interval=None) as websocket:
				while True:
					_, self.frame = self.cap.read()
					self.buff = self.frame
					self.mjpeg.send_stream(self.buff)
					#a_t.pose_estimation(buff)
					websocket.send(str(self.mjpeg.bw))
		except Exception as exc:
			print(f"Client error: {exc!r}")
		finally:
			self.shm.close()
			self.shm.unlink()

