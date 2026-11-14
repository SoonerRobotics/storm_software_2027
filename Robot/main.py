from robot import Robot
import websockets
import asyncio
from multiprocessing import shared_memory
import sys, cv2
from json import loads
from Mechanisms.cannon import Cannon	

async def main():
	
	cap = cv2.VideoCapture(0)
	_, frame = cap.read()
	#just getting the memory size of camera frames so we can make a big enough shared memory
	shm = shared_memory.SharedMemory(name = "Frame5", create=True, size=sys.getsizeof(frame))
	cap.release()
	buf = shm.buf
	robot = Robot(shm, buf)
	cannon = Cannon()
	try:
		robot.start()
		while True:
			#send mjpeg with http stuff
			robot.send_camera()
			#send bandwidth with websockets
			robot.send_bw()
			msg = loads(robot.ws.recv())
			#this is how i'm thinking of passing commands to various systems, just match case dictionary values
			match msg["Header"]:
				case "Cannon":
					cannon.cannon = msg["Message"]
					cannon.shoot()
	except Exception as e:
		print(f"Something broke: {e}")
	finally:
		shm.close()
		shm.unlink()

  

if __name__ == "__main__":
	asyncio.run(main())