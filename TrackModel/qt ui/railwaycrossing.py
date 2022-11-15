class RailwayCrossing:
    def __init__(self):
        self.state = False

    def get_state(self):
        return self.state

    def set_state(self, s):
        self.state = s