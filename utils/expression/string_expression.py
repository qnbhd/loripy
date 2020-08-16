from .expression import Expression


class StringExpression(Expression):
    string: str

    def __init__(self, string):
        super().__init__()
        self.string = string

    def __str__(self):
        return f"<(STRING EXPRESSION)> :: {self.string}"

    def __repr__(self):
        return self.__str__()

    def execute(self):
        return self.string
