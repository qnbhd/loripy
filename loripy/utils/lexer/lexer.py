from typing import List, Tuple

from .lexer_exception import LexerException
from .lined_token import LinedToken
from .sifter import Sifter
from .token import Token
from .token_type import TokenType


class Lexer:
    code: List[Tuple[str, int]]
    tokens: List[LinedToken]

    def __init__(self, source="", source_type='string'):
        src = source
        if source_type == 'file':
            with open(source, 'r', encoding='utf-8') as fin:
                src = fin.read()
        elif source_type != 'string':
            raise TypeError('Invalid source type')
        self.code = Sifter(src).sift()
        self.tokens = []

    def tokenize(self) -> List[LinedToken]:
        buffer = ""
        record_string = False
        last_line = 1
        for i, tup in enumerate(self.code):
            sym, line = tup
            last_line = line
            if sym == "\"":
                record_string = not record_string
            if self.is_sep(sym):
                buffer = self.sep_tk_case(sym, buffer, line, record_string)
            else:
                buffer += sym

        if buffer != "":
            self.tokens.append(LinedToken(buffer, last_line))

        self.adj_sub()
        return self.tokens

    def sep_tk_case(self, sym, buffer, line, record_string):
        if buffer != "":
            self.tokens.append(LinedToken(buffer, line))
            return ""
        if record_string or (sym != " " and sym != '\n' and sym != '\t'):
            self.tokens.append(LinedToken(sym, line))
        return buffer

    def adj_decimal_handler(self, i, line, hatch_tokens) -> int:
        token = LinedToken(self.tokens[i].lexeme +
                           self.tokens[i + 1].lexeme +
                           self.tokens[i + 2].lexeme, line)
        hatch_tokens.append(token)
        return i + 3

    def adj_operator_handler(self, i, line, hatch_tokens) -> int:
        token = LinedToken(self.tokens[i].lexeme +
                           self.tokens[i + 1].lexeme, line)
        hatch_tokens.append(token)
        return i + 2

    def adj_string_handler(self, i, line, hatch_tokens) -> int:
        buffer = self.tokens[i].lexeme
        adj_half = self.get_adj_half(self.tokens[i])
        i += 1
        while i < len(self.tokens):
            buffer += self.tokens[i].lexeme
            if self.tokens[i].type == adj_half or \
                    (len(self.tokens[i].lexeme) == 1 and
                     self.tokens[i].type == TokenType.STRING_CONST):
                token = LinedToken(buffer, line)
                hatch_tokens.append(token)
                break
            i += 1
        else:
            raise LexerException("[RIGHT HALF OF ADJUSTABLE OPERATOR"
                                 + str(adj_half) + "EXPECTED]")
        i += 1
        return i

    def adj_default_handler(self, i, line, hatch_tokens) -> int:
        hatch_tokens.append(LinedToken(self.tokens[i].lexeme, line))
        return i + 1

    def adj_handler_get(self, i):
        if i < len(self.tokens) - 2 and \
                self.is_adj_decimal(self.tokens[i], self.tokens[i + 1]):
            return self.adj_decimal_handler
        elif i < len(self.tokens) - 1 and \
                self.is_adj_operator(self.tokens[i], self.tokens[i + 1]):
            return self.adj_operator_handler
        elif self.tokens[i].type == TokenType.LEFT_STRING:
            return self.adj_string_handler
        else:
            return self.adj_default_handler

    def adj_sub(self):
        hatch_tokens = []
        i = 0
        while i < len(self.tokens):
            line = self.tokens[i].line
            adj_handler = self.adj_handler_get(i)
            i = adj_handler(i, line, hatch_tokens)

        self.tokens = hatch_tokens

    def print(self):
        print('------- Token Table -------')

        for token in self.tokens:
            print(token)

    @staticmethod
    def is_adj_decimal(first: Token, second: Token) -> bool:
        return first.type == TokenType.NUMBER_CONST and \
               second.type == TokenType.POINT

    @staticmethod
    def get_adj_half(first: Token) -> TokenType:
        if first.type == TokenType.LEFT_STRING:
            return TokenType.RIGHT_STRING
        if first.type == TokenType.LEFT_MULTI_LINE_COMMENT:
            return TokenType.RIGHT_MULTI_LINE_COMMENT
        return TokenType.NONE

    @staticmethod
    def is_adj_operator(first: Token, second: Token) -> bool:
        return (first.lexeme in "<>=+-*/:!" and second.lexeme == "=") or \
               (first.lexeme == "+" and second.lexeme == "+") or \
               (first.lexeme == "-" and second.lexeme == "-") or \
               (first.lexeme == "/" and second.lexeme == "*") or \
               (first.lexeme == "*" and second.lexeme == "/") or \
               (first.lexeme == "&" and second.lexeme == "&") or \
               (first.lexeme == "|" and second.lexeme == "|")

    @staticmethod
    def is_sep(sym) -> bool:
        return sym in " ()+-*/<>{}=!:;.,\n\t\r"
