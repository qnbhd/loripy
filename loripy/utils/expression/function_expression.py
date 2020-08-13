from .expression import Expression


class FunctionExpression(Expression):
    function: str
    expression: Expression

    def __init__(self, function, expression):
        super().__init__()
        self.function = function
        self.expression = expression

    def __str__(self):
        return f"<(Function Expression)> :: {str(self.expression)} FUNC: {self.function}"

    def __repr__(self):
        return self.__str__()

    def execute(self):
        return self.expression.execute()
