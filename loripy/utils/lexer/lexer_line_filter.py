from typing import Dict
from .lined_token import LinedToken

class LexerLineFilter:

    def __init__(self, tokens_from_lexer):
        self.tokens = tokens_from_lexer

    def get_filtered_tokens(self):
        filtered_tokens: Dict[list] = dict()

        for lined_token in self.tokens:
            line = lined_token.line
            filtered_tokens[line] = list()

        for lined_token in self.tokens:
            token_type = lined_token.type
            lexeme = lined_token.lexeme
            line = lined_token.line

            filtered_tokens[line].append(lined_token)

        return filtered_tokens
