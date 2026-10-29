
#TODO FIXME

import time

from Robot.robot import Robot

#TODO FIXME who is controlled / responding to FMS messages and commands?

if __name__ == "__main__":
    robot = Robot()

    while not robot.connected:
        #TODO this is an example
        robot.connect()
        time.sleep(1)

    # robot is now connected
    robot.start()

    try:
        while True:
            #FIXME doesn't this need to be CommandScheduler.run()
            robot.loop()

            # we should copy and have like a RobotInit, RobotPeriodic, AutonomousInit, AutonomousPeriodic, etc.
    except Exception as e:
        print(f"Robot enountered exception: {e}")

        robot.close()

        raise e