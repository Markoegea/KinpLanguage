from typing import List
import readline

from kp.ast import Program
from kp.lexer import Lexer
from kp.parser import Parser
from kp.token import (
    Token,
    TokenType,
)
from kp.evaluator import evaluate

EOF_TOKEN: Token = Token(TokenType.EOF,'')

def _print_parse_errors(errors: List[str]):
    for error in errors:
        print(error)

def star_repl() -> None:
    while (source := input('-> ')) != 'salir()':
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()
        if len(parser.errors) > 0:
            _print_parse_errors(parser.errors)
            continue

        evaluated = evaluate(program)
        assert evaluated is not None
        if evaluate is not None:
            print(evaluated.inspect())