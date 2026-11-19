class Traversal:
    def __init__(self, el):
        self.el = el

    def drive(self, forward: float, turn: float):
        # update our vars
        self.el.update_vars({
            "forward": forward,
            "turn": turn
        })
        self.el.send_msg()

    def stop(self):
        # stop the robot by sending 0 directly to forward and turn.
        # TODO make sure that sending 0 stops the robot in place and doesn't try to like reset it
        self.drive(0, 0)
