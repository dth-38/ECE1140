class Failure:
    def __init__(self):
        self.state = FALSE
        self.type = ''

    def set_state(self, fail):
        self.state = fail

    def set_type(self, fail):
        fl = fail.lower()
        if ((fl == "power") OR (fl == "broken rail") OR ("track circuit") {
            self.type = fl
        } else {
            print("Invalid failure type")
            self.set_type(fail)
        }