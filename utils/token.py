from .token_type import TokenType
from .tokens_map import TokensMap


class Token:
    lexeme: str
    type: TokenType

    def __init__(self, lexeme_: str):
        self.lexeme = lexeme_
        self.type = self.wto(lexeme_)

    def wto(self, lexeme: str) -> TokenType:
        if self.is_string(lexeme):
            return TokenType.STRING_CONST
        if self.is_left_string(lexeme):
            return TokenType.LEFT_STRING
        if self.is_right_string(lexeme):
            return TokenType.RIGHT_STRING

        temporary = TokensMap.map.get(lexeme)
        if temporary is not None:
            return temporary
        if self.is_number(lexeme):
            return TokenType.NUMBER_CONST

        return TokenType.IDENTIFIER

    @staticmethod
    def is_number(lexeme: str) -> bool:
        for sym in lexeme:
            if not sym.isdigit() and sym != '.':
                return False
        return True

    @staticmethod
    def is_left_string(lexeme: str) -> bool:
        return lexeme[0] == "\""

    @staticmethod
    def is_right_string(lexeme: str) -> bool:
        return lexeme[-1] == "\""

    @staticmethod
    def is_string(lexeme: str) -> bool:
        if lexeme[0] == "\"" and lexeme[-1] == "\"":
            return True
        return False

    def name(self):
        type_str = str(self.type)
        token_type = type_str[:type_str.find('.')]
        return token_type

    def __str__(self):
        token_type = self.name()
        return "<(" + token_type + ", " + self.lexeme + ")>"

    def __repr__(self):
        return self.__str__()


