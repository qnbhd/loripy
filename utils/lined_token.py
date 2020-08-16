from .token import Token


class LinedToken(Token):
    line: int

    def __init__(self, lexeme_: str, line: int):
        super().__init__(lexeme_)
        self.line = line

    def name(self):
        type_str = str(self.type)
        token_type = type_str[type_str.find('.') + 1:]
        return token_type

    def __str__(self):
        token_type = self.name()
        return "{::" + \
               token_type + ", '" + \
               self.lexeme + "', " + str(self.line) + \
               "}"

    def __repr__(self):
        return self.__str__()
