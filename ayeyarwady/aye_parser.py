import tokens as t
import aye_ast
import ayeyarwady.types as aye_types

from llvmlite import ir
from rply import ParserGenerator


class Parser:
    def __init__(self, module, builder):
        self.pg = ParserGenerator(
            t.ALL_TOKENS,
            precedence=[
                ("left", [t.SUM, t.SUB]),
                ("left", [t.DIV, t.MUL]),
            ],
        )
        self.module = module
        self.builder = builder
        self.printf = self._get_print_function()

    def _get_print_function(self):
        return ir.Function(
            self.module,
            ir.FunctionType(aye_types.INT8, [], var_arg=True),
            name='printf',
        )

    def parse(self):
        @self.pg.production('program : statement')
        @self.pg.production('program : program statement')
        def program(p):
            return aye_ast.Program(p)

        @self.pg.production(f'statement : {t.PRINT} OPEN_PAREN expression CLOSE_PAREN')
        def printf(p):
            return aye_ast.Print(self.builder, self.module, p[2], self.printf)

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

        @self.pg.production(f'expression : {t.DOUBLE}')
        def double(p):
            return aye_ast.Double(self.builder, self.module, p[0].value)

        @self.pg.production(f'expression : {t.STRING}')
        def string(p):
            return aye_ast.String(self.builder, self.module, p[0].value)

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
