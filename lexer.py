import tokens as t

from rply import LexerGenerator


class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Print
        self.lexer.add(t.PRINT, r'print')
        # Parenthesis
        self.lexer.add(t.OPEN_PAREN, r'\(')
        self.lexer.add(t.CLOSE_PAREN, r'\)')
        # Operators
        self.lexer.add(t.SUM, r'\+')
        self.lexer.add(t.SUB, r'\-')
        # Number
        self.lexer.add(t.NUMBER, r'\d+')
        # Ignore spaces
        self.lexer.ignore('\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
