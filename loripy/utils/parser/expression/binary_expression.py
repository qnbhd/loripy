from .expression import Expression


class BinaryExpression(Expression):
    expr1: Expression
    expr2: Expression
    operation: str

    def __init__(self, operation, expr1, expr2):
        super().__init__()
        self.operation = operation
        self.expr1 = expr1
        self.expr2 = expr2

    def __str__(self):
        return f"<(BINARY EXPRESSION)> :: {str(self.expr1)} WITH {str(self.expr2)} OP: {self.operation}"

    def __repr__(self):
        return self.__str__()

    def execute(self):
        left = self.expr1.execute()
        right = self.expr2.execute()
        operation = self.operation

        if operation == '-':
            return left - right
        elif operation == '*':
            return left * right
        elif operation == '/':
            if right == 0.0:
                raise ZeroDivisionError('Zero division error')
            return left / right
        else:
            # default
            return left + right
