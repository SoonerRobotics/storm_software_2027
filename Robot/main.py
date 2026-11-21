from Mechanisms import traversal, electrical_interface
from robot import Robot
import asyncio
from multiprocessing import shared_memory
import sys, cv2
from json import loads
from Mechanisms.cannon import Cannon	

async def main():
	
	cap = cv2.VideoCapture(0)
	_, frame = cap.read()
	shm = shared_memory.SharedMemory(name = "Frame5", create=True, size=sys.getsizeof(frame))
	cap.release()
	buf = shm.buf
	robot = Robot(shm, buf)
	electrical = electrical_interface.Electrical_Interface()
	cannon = Cannon(electrical)
	traverse = traversal.Traversal(electrical)
	try:
		robot.start()
		while True:
			robot.send_camera()
			robot.send_bw()
			msg = loads(robot.ws.recv())
			match msg["Header"]:
				# we use the websocket event to determine what to do here
				case "Cannon":
					action = msg["Message"]
					if action["type"] == "move":
						cannon.move(action["x"], action["y"])
					elif action["type"] == "shoot":
						cannon.shoot()
				case "Traversal":
					action = msg["Message"]
					if action["type"] == "drive":
						# we are using forward and turn commands here
						# forward is positive, backwards is negative
						# turning left is negative, turning right is positive
						traverse.drive(action["forward"], action["turn"])
					elif action["type"] == "stop":
						# this just writes 0 to our serial interface to halt the robot
						traverse.stop()

	except Exception as e:
		print(f"Something broke: {e}")
	finally:
		shm.close()
		shm.unlink()

  

if __name__ == "__main__":
	asyncio.run(main())