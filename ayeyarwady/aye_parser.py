import tokens as t
import aye_ast

from rply import ParserGenerator


class Parser:
    def __init__(self, module, builder, printf):
        self.pg = ParserGenerator(
            t.ALL_TOKENS,
            precedence=[("left", [t.SUM, t.SUB])],
        )
        self.module = module
        self.builder = builder
        self.printf = printf

    def parse(self):
        @self.pg.production(f'program : {t.PRINT} OPEN_PAREN expression CLOSE_PAREN')
        def program(p):
            return aye_ast.Print(self.builder, self.module, self.printf, p[2])

        @self.pg.production(f'expression : expression {t.SUM} expression')
        @self.pg.production(f'expression : expression {t.SUB} expression')
        @self.pg.production(f'expression : expression {t.MUL} expression')
        @self.pg.production(f'expression : expression {t.DIV} expression')
        def expression(p):
            left = p[0]
            right = p[2]
            operator_token_type = p[1].gettokentype()

            if operator_token_type == t.SUM:
                class_ = aye_ast.Sum
            elif operator_token_type == t.SUB:
                class_ = aye_ast.Sub
            elif operator_token_type == t.MUL:
                class_ = aye_ast.Mul
            elif operator_token_type == t.DIV:
                class_ = aye_ast.Div
            else:
                raise ValueError(f'Unknown operator: {p[1]}')

            return class_(self.builder, self.module, left, right)

        @self.pg.production(f'expression : {t.INTEGER}')
        def integer(p):
            return aye_ast.I32(self.builder, self.module, p[0].value)

        @self.pg.production(f'expression : {t.FLOAT}')
        def float_(p):
            return aye_ast.Float(self.builder, self.module, p[0].value)

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
