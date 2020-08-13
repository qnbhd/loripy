from .token_type import TokenType


class TokensMap:
    map = {
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "*": TokenType.STAR,
        "/": TokenType.SLASH,
        "+=": TokenType.ADD_ASSIGN,
        "-=": TokenType.SUB_ASSIGN,
        "*=": TokenType.MUL_ASSIGN,
        "/=": TokenType.DIV_ASSIGN,
        "++": TokenType.INCREMENT,
        "--": TokenType.DECREMENT,

        "for": TokenType.FOR,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "switch": TokenType.SWITCH,

        "(": TokenType.LPAREN,
        ")": TokenType.RPAREN,
        "[": TokenType.LSQ,
        "]": TokenType.RSQ,
        "{": TokenType.LBRA,
        "}": TokenType.RBRA,
        ":": TokenType.COLON,
        ";": TokenType.SEMICOLON,

        "return": TokenType.RETURN,
        "continue": TokenType.CONTINUE,
        "break": TokenType.BREAK,

        "=": TokenType.ASSIGN,
        "<": TokenType.LESS,
        ">": TokenType.GREATER,

        "==": TokenType.EQUAL,
        "!=": TokenType.NOT_EQUAL,
        "<=": TokenType.LESS_OR_EQUAL,
        ">=": TokenType.GREATER_OR_EQUAL,

        ":=": TokenType.COLON_ASSIGN,

        ".": TokenType.POINT,
        "!": TokenType.EXCLAMATION,
        "?": TokenType.QUESTION,
        ",": TokenType.COMMA,

        '\0': TokenType.EOF,

        "//": TokenType.ONE_LINE_COMMENT,
        "/*": TokenType.LEFT_MULTI_LINE_COMMENT,
        "*/": TokenType.RIGHT_MULTI_LINE_COMMENT,

        "||": TokenType.OR,
        "&&": TokenType.AND,

        "[$": TokenType.STARTCODE,
        "$]": TokenType.ENDCODE,

    }
