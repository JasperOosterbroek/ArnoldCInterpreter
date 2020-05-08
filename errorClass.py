class Error:
    def __init__(self,  message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return "{}".format(self.message)

    def __repr__(self) -> str:
        return str(self)


class SyntaxError(Error):

    def __init__(self, message: str) -> None:
        super().__init__(message)

    def __str__(self):
        return "Syntax Error: {}".format(super().__str__())


class ParseError(Error):

    def __init__(self, message: str) -> None:
        super().__init__(message)

    def __str__(self) -> str:
        return "Parse Error: {}".format(super().__str__())


class RuntimeError(Error):

    def __init__(self, message: str) -> None:
        super().__init__(message)

    def __str__(self) -> str:
        return "Runtime Error: {}".format(super().__str__())
