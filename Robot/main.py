from robot import Robot
import websockets
import asyncio
from multiprocessing import shared_memory
import sys, cv2

async def main():
	
	cap = cv2.VideoCapture(0)
	_, frame = cap.read()
	shm = shared_memory.SharedMemory(name = "Frame5", create=True, size=sys.getsizeof(frame))
	cap.release()
	buf = shm.buf
	robot = Robot(shm, buf)
	try:
		robot.start()
		while True:
			robot.send_camera()
			robot.send_bw()
			#print(robot.ws.recv())
	except Exception as e:
		print(f"Something broke: {e}")
	finally:
		shm.close()
		shm.unlink()

  

if __name__ == "__main__":
	asyncio.run(main())