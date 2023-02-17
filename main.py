import pathlib
from lexer import Lexer
from syntax_parser import Parser
from codegen import CodeGen


def main():
    text_input = pathlib.Path("code_examples/input.aye").read_text()

    lexer = Lexer().get_lexer()
    tokens = lexer.lex(text_input)

    codegen = CodeGen()

    module = codegen.module
    builder = codegen.builder
    printf = codegen.printf

    pg = Parser(module, builder, printf)
    pg.parse()
    parser = pg.get_parser()
    parser.parse(tokens).eval()

    codegen.create_ir()
    codegen.save_ir("build/output.ll")


if __name__ == '__main__':
    main()
