import argparse
import pathlib

from lexer import Lexer
from aye_parser import Parser
from codegen import CodeGen

DEFAULT_FILE = 'code_examples/input.aye'


def main(file: str = None):
    text_input = pathlib.Path(file or DEFAULT_FILE).read_text()

    lexer = Lexer().get_lexer()
    tokens = lexer.lex(text_input)

    codegen = CodeGen()

    module = codegen.module
    builder = codegen.builder

    pg = Parser(module, builder)
    pg.parse()
    parser_ = pg.get_parser()
    parser_.parse(tokens).eval()

    codegen.create_ir()
    codegen.save_ir("build/output.ll")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file')
    args_ = parser.parse_args()

    main(args_.file)
