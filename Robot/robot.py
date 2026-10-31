from Camera.driver_camera import Camera

class Robot():
    def __init__(self):
        self.cam = Camera()
    
    def start(self):
        self.cam.run_camera()