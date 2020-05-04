class Error:
    def __init__(self,  message):
        self.message = message

    def __str__(self):
        return "{}".format(self.message)

    def __repr__(self):
        return str(self)


class SyntaxError(Error):

    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return "Syntax Error: {}".format(super().__str__())


class ParseError(Error):

    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return "Parse Error: {}".format(super().__str__())


class RuntimeError(Error):

    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return "Runtime Error: {}".format(super().__str__())
