
#TODO

from Robot.electrical.cannon import CannonBoard
from Robot.electrical.electrical_interface import ElectricalInterface
from Robot.electrical.traversal import TraversalBoard

from Robot.hardware.climber import Climber
from Robot.hardware.drivetrain import Drivetrain
from Robot.hardware.indexer import Indexer
from Robot.hardware.intake import Intake
from Robot.hardware.shooter import Shooter
from Camera.driver_camera import Camera


class Robot:
    def __init__(self):
        self.connected = False

        self.electrical_interface = ElectricalInterface()

        self.traversal_board = TraversalBoard(self.electrical_interface)
        self.cannon_board = CannonBoard(self.electrical_interface)

        self.climber = Climber(self.traversal_board)
        self.drivetrain = Drivetrain(self.traversal_board)

        self.shooter = Shooter(self.cannon_board)
        self.intake = Intake(self.cannon_board)
        self.indexer = Indexer(self.cannon_board)

    def start(self):
        self.electrical_interface.open()

        #TODO who is spinning up the separate electrical thread?

        pass #TODO

    def connect(self):
        pass #TODO connect to GUI?
        cam = Camera()
        cam.run_camera()

    def close(self):
        pass #TODO: idk close logs? other resources?

    def loop(self):
        pass #TODO idk all robot logic go here??????