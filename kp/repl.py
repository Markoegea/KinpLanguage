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
from kp.object import Environment

EOF_TOKEN: Token = Token(TokenType.EOF,'')

def _print_parse_errors(errors: List[str]):
    for error in errors:
        print(error)

def star_repl() -> None:
    scanned: List[str] = []
    while (source := input('-> ')) != 'salir()':
        scanned.append(source)
        lexer: Lexer = Lexer(' '.join(scanned))
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()
        env: Environment = Environment()
        if len(parser.errors) > 0:
            _print_parse_errors(parser.errors)
            continue

        evaluated = evaluate(program,env)
        #assert evaluated is not None
        if evaluated is not None:
            print(evaluated.inspect())