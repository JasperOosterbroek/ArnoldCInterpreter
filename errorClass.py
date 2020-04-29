class Error:
    def __init__(self, type, message):
        self.type = type
        self.message = message

    def __str__(self):
        return "{}: {}".format(self.type, self.message)

    def __repr__(self):
        return str(self)