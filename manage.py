import argparse
from loripy.utils.lexer.lexer import Lexer

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Loripy - templating language for Python'
    )
    parser.add_argument('filename', help='filename')
    args = parser.parse_args()
    filename = args.filename

    lexer = Lexer(filename, source_type='file')
    result = lexer.tokenize()

    lexer.print()
