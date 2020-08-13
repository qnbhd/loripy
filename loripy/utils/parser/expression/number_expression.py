from .expression import Expression


class NumberExpression(Expression):
    value: int

    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return f'<(NUMBER EXPRESSION)> :: {self.value}'

    def __repr__(self):
        return self.__str__()

    def execute(self):
        return self.value
