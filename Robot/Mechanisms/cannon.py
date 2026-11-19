class Cannon:
    def __init__(self, el):
        self.el = el
    def move(self, x, y):
        # just update our variables and send that to our serial interface
        self.el.update_vars({
            'cannon_x': x,
            'cannon_y': y
        })
        self.el.send_msg()
    def shoot(self):
        # shoot the cannon!!!
        self.el.send_command("cannon_fire")