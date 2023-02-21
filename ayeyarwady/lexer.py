import tokens as t

from rply import LexerGenerator


class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Keywords
        self.lexer.add(t.PRINT, r'print')

        # Parenthesis
        self.lexer.add(t.OPEN_PAREN, r'\(')
        self.lexer.add(t.CLOSE_PAREN, r'\)')
        self.lexer.add(t.OPEN_CURLY_BRACKET, r'\{')
        self.lexer.add(t.CLOSE_CURLY_BRACKET, r'\}')

        # Operators
        self.lexer.add(t.SUM, r'\+')
        self.lexer.add(t.SUB, r'\-')
        self.lexer.add(t.SUB, r'\*')
        self.lexer.add(t.SUB, r'\\')

        # Types
        self.lexer.add(t.DOUBLE, r'-?\d+\.\d+')
        self.lexer.add(t.INTEGER, r'-?\d+')
        self.lexer.add(t.STRING, '(""".?""")|(".?")|(\'.?\')')

        # Ignore spaces
        # maybe [\t\r\n\f\s]+ ?
        self.lexer.ignore('\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
