from .expression import Expression
from .operation_exception import OperationException


class UnaryExpression(Expression):
    expr1: Expression
    operation: str

    def __init__(self, operation, expr1):
        super().__init__()
        self.operation = operation
        self.expr1 = expr1

    def __str__(self):
        return f"<(UNARY EXPRESSION)> {str(self.expr1)} OP: {self.operation}"

    def __repr__(self):
        return self.__str__()

    def execute(self):
        right = self.expr1.execute()
        operation = self.operation

        if operation == '-':
            return -right
        elif operation == '+':
            return right
        else:
            raise OperationException('Not found operation for unary expression, +/- expected')
