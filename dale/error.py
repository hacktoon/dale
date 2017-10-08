

class SyntaxError(Exception):
    def __init__(self, message, line, column):
        self.line = line
        self.column = column
        super().__init__(message)


class ParserError(Exception):
    pass
