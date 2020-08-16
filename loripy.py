from utils.lexer import Lexer
from utils.parser import Parser
from bs4 import BeautifulSoup as bs
from utils.sandbox import SandBox
import re
import webbrowser

orig_prettify = bs.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)


def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))


bs.prettify = prettify


class Loripy:
    source: str
    sandbox: SandBox
    expressions: dict

    def __init__(self, source, source_type='string'):
        self.source = source
        self.sandbox = SandBox()
        if source_type == 'file':
            with open(source, encoding="utf-8") as f:
                self.source = f.read()
                f.seek(0)
                self.lines = f.readlines()
        elif source_type != 'string':
            raise TypeError('Invalid source type')
        self.expressions = dict()

    def process(self):
        lexer = Lexer(self.source)
        lexer_result = lexer.tokenize()
        parser = Parser(lexer_result, self.sandbox)
        self.expressions = parser.parse()

    def render(self, destination, prettify=False):
        for item in self.expressions.items():
            line, expression = item
            line_index_in_file = line - 1
            content_on_line = self.lines[line_index_in_file]
            executed_result = str(expression.execute())

            start_code_pos = content_on_line.find('[$')
            if start_code_pos == -1:
                raise Exception('Undefined exception in analyze')
            end_code_pos = content_on_line.find('$]') + 1

            left = content_on_line[:start_code_pos]
            right = content_on_line[end_code_pos + 1:]
            result = left + executed_result + right

            self.lines[line_index_in_file] = result

        rendered_html = ' '.join(self.lines)
        soup = bs(rendered_html, 'html.parser')

        if prettify:
            rendered_html = soup.prettify(formatter='html', indent_width=2)

        with open(destination, 'w', encoding="utf-8") as f:
            f.write(rendered_html)

        webbrowser.open_new_tab(destination)
