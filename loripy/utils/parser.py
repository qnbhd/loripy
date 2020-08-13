from typing import List

from loripy.utils.expression.binary_expression import BinaryExpression
from loripy.utils.expression.expression import Expression
from loripy.utils.expression.expression_exception import ExpressionException
from loripy.utils.expression.number_expression import NumberExpression
from loripy.utils.expression.string_expression import StringExpression
from loripy.utils.expression.unary_expression import UnaryExpression
from loripy.utils.lexer_line_filter import LexerLineFilter
from loripy.utils.lined_token import LinedToken
from loripy.utils.token import Token
from loripy.utils.token_type import TokenType


class Parser:
    not_filtered_tokens: [LinedToken]
    tokens: [List[LinedToken]]
    CUR_LINE: int

    def __init__(self, tokens):
        self.not_filtered_tokens = tokens
        self.tokens = LexerLineFilter(tokens).get_filtered_tokens()
        self.pos = 0
        self.CUR_LINE = 0

    def get(self, relative_position: int) -> LinedToken:
        position = self.pos + relative_position
        if position >= len(self.tokens[self.CUR_LINE]):
            return LinedToken('\0', 0)
        return self.tokens[self.CUR_LINE][position]

    def match(self, type_: TokenType) -> bool:
        current = self.get(0)
        if type_ != current.type:
            return False

        self.pos += 1
        return True

    def consume(self, type_: TokenType) -> Token:
        current = self.get(0)

        if type_ != current.type:
            raise RuntimeError("Token " + str(current) + " doesn't match " + str(type_))

        self.pos += 1
        return current

    def parse(self):
        result = {line: Expression() for line in self.tokens}

        for line, code_block in self.tokens.items():
            self.pos = 0
            self.CUR_LINE = line
            res = self.CODE_BLOCK()
            result[line] = res

        return result

    def CODE_BLOCK(self) -> Expression:
        self.consume(TokenType.STARTCODE)
        result = self.EXPRESSION()
        self.consume(TokenType.ENDCODE)
        return result

    def EXPRESSION(self) -> Expression:
        return self.ADD()

    def ADD(self) -> Expression:
        result = self.MULT()

        while True:
            if self.match(TokenType.PLUS):
                result = BinaryExpression('+', result, self.MULT())
                continue
            if self.match(TokenType.MINUS):
                result = BinaryExpression('-', result, self.MULT())
                continue
            break

        return result

    def MULT(self) -> Expression:
        result = self.UNARY()

        while True:
            if self.match(TokenType.STAR):
                result = BinaryExpression('*', result, self.UNARY())
                continue
            if self.match(TokenType.SLASH):
                result = BinaryExpression('/', result, self.UNARY())
                continue
            break

        return result

    def UNARY(self) -> Expression:
        if self.match(TokenType.MINUS):
            return UnaryExpression('-', self.PRIMARY())
        return self.PRIMARY()

    def decimal_match(self, current) -> Expression:
        is_int = True if current.lexeme.find('.') == -1 else False
        if is_int:
            return NumberExpression(int(current.lexeme))
        return NumberExpression(float(current.lexeme))

    def string_match(self, current) -> Expression:
        return StringExpression(current.lexeme)

    def identifier_match(self, current) -> Expression:
        return Expression()

    def PRIMARY(self) -> Expression:
        current = self.get(0)

        if self.match(TokenType.NUMBER_CONST):
            return self.decimal_match(current)

        if self.match(TokenType.STRING_CONST):
            return self.string_match(current)

        if self.match(TokenType.IDENTIFIER):
            return self.identifier_match(current)

        raise ExpressionException('Unknown expression')
