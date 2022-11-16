class Failure:
    def __init__(self):
        self.state = False
        self.type = ''

    def set_state(self, fail):
        self.state = fail

    def get_state(self):
        return self.state

    def set_type(self, fail):
        fl = fail.lower()
        if (fl == "power") or (fl == "broken rail") or ("track circuit"):
            self.type = fl
        else:
            print("Invalid failure type")
            self.set_type(fail)