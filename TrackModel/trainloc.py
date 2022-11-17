class TrainLoc:
    def __init__(self, t):
        self.line = None
        self.block = None
        self.train = t
        self.current_position = 0
        self.old_position = 0

    def new_train_position(self):
        self.old_position = self.current_position
        
