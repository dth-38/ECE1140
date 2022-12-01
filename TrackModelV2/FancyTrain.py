from TrainModel.Train import Train


class FancyTrain(Train):
    
    def __init__(self, id=0):
        super().__init__(id)

        self.position_in_block = 0
        self.line = ""
        self.block = 0
        self.movement_direction = 1