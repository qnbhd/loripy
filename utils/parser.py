import collections

from typing import List
from utils.expression.binary_expression import BinaryExpression
from utils.expression.expression import Expression
from utils.expression.expression_exception import ExpressionException
from utils.expression.number_expression import NumberExpression
from utils.expression.string_expression import StringExpression
from utils.expression.unary_expression import UnaryExpression
from utils.lexer_line_filter import LexerLineFilter
from utils.lined_token import LinedToken
from utils.sandbox_exception import SandBoxException
from utils.token import Token
from utils.token_type import TokenType


class Parser:
    not_filtered_tokens: [LinedToken]
    tokens: [List[LinedToken]]
    CUR_LINE: int

    def __init__(self, tokens, sandbox):
        self.not_filtered_tokens = tokens
        self.tokens = LexerLineFilter(tokens).get_filtered_tokens()
        self.pos = 0
        self.sandbox = sandbox

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
        result = {line: [] for line in self.tokens}
        blocks_count_on_lines = collections.Counter()

        for line, code_block in self.tokens.items():
            for token in code_block:
                if token.type == TokenType.STARTCODE:
                    blocks_count_on_lines[line] += 1

        for line, code_block in self.tokens.items():
            self.pos = 0
            self.CUR_LINE = line
            for iteration in range(blocks_count_on_lines[line]):
                res = self.CODE_BLOCK()
                result[line].append(res)

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
        string = current.lexeme[1:-1]
        return StringExpression(string)

    def identifier_match(self, current) -> Expression:
        identifier_name = current.lexeme
        value = None
        try:
            value = self.sandbox.get_variable(identifier_name)
        except SandBoxException:
            pass
        try:
            value = self.sandbox.get_function(identifier_name)
        except SandBoxException:
            pass
        if value is None:
            raise SandBoxException("Identifier doesn't exist in sandbox")
        if isinstance(value, int):
            return NumberExpression(value)
        return StringExpression(value)

    def PRIMARY(self) -> Expression:
        current = self.get(0)

        if self.match(TokenType.NUMBER_CONST):
            return self.decimal_match(current)

        if self.match(TokenType.STRING_CONST):
            return self.string_match(current)

        if self.match(TokenType.IDENTIFIER):
            return self.identifier_match(current)

        print(current)
        raise ExpressionException('Unknown expression')
