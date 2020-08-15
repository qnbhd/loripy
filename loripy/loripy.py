from loripy.utils.lexer import Lexer
from loripy.utils.parser import Parser
from bs4 import BeautifulSoup as bs
from loripy.utils.sandbox import SandBox
import re
import webbrowser

orig_prettify = bs.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)


def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))


bs.prettify = prettify


class Loripy:

    def __init__(self, source, source_type='string'):
        self.source = source
        self.sandbox = SandBox()
        if source_type == 'file':
            with open(source) as f:
                self.source = f.read()
                f.seek(0)
                self.lines = f.readlines()
        elif source_type != 'string':
            raise TypeError('Invalid source type')

        lexer = Lexer(self.source)
        self.sandbox.add_variable('var', 'Gavr chlen')
        lexer_result = lexer.tokenize()
        parser = Parser(lexer_result, self.sandbox)
        self.expressions = parser.parse()

    def render(self, destination):
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

        # prettyHTML = soup.prettify(formatter='html', indent_width=3)

        with open(destination, 'w') as f:
            f.write(rendered_html)

        webbrowser.open_new_tab(destination)

