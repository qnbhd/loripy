from enum import Enum
from typing import List, Tuple

from .line_exception import LineException


class Sifter:
    class State(Enum):
        READ = 1,
        PASS = 2,

    def __init__(self, code):
        self.code = code
        self.line = 1
        self.state = Sifter.State.PASS
        self.pos = 0

    def __len__(self):
        return len(self.code)

    def seek(self, seek=1) -> bool:
        if self.pos + seek < len(self) + 1:
            self.pos += seek
            return True
        return False

    def get(self, seek=0) -> str:
        return self.code[self.pos + seek]

    def get_next(self):
        return self.get(1)

    def get_prev(self):
        return self.get(-1)

    def start_code_handler(self, current_line, sifted) -> str:
        if self.get() == '[' and self.get_next() == '$':
            self.state = Sifter.State.READ
            current_line = self.line
        return current_line

    def appender_handler(self, current_line, sifted) -> str:
        if self.state == Sifter.State.READ:
            if current_line != self.line:
                raise LineException(
                    "There should be no line breaks in the code block"
                )
            sifted.append((self.get(), self.line))
        return current_line

    def end_code_handler(self, current_line, sifted) -> str:
        if self.get() == ']' and self.get_prev() == '$':
            self.state = Sifter.State.PASS
        return current_line

    def line_breaker_handler(self, current_line, sifted) -> str:
        if self.get() == '\n':
            sifted.append(('\n', self.line))
            self.line += 1
        return current_line

    def sift(self) -> List[Tuple[str, int]]:
        sifted = []
        current_line = 1
        while self.pos < len(self.code):
            current_line = self.start_code_handler(current_line, sifted)
            current_line = self.appender_handler(current_line, sifted)
            current_line = self.end_code_handler(current_line, sifted)
            current_line = self.line_breaker_handler(current_line, sifted)
            self.seek()
        return sifted
