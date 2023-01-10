import readline
from typing import List

from kp.ast import Program
from kp.lexer import Lexer
from kp.parser import Parser
from kp.token import (
    Token,
    TokenType,
)
from kp.evaluator import evaluate
from kp.object import (Environment, Error)

EOF_TOKEN: Token = Token(TokenType.EOF,'')

_FILENOTFOUND = 'Poseemos un problema, no se encontro el archivo {}'

#Imprimir los errores en pantalla
def _print_parse_errors(errors: List[str]):
    for error in errors:
        print(error)

#Iniciar todos los elementos necesarios apartir del input, y de esta manera correr el programa
def star_repl(source: str, scanned: List[str]) -> None:
    scanned.append(source)
    lexer: Lexer = Lexer(' '.join(scanned))
    parser: Parser = Parser(lexer)
    program: Program = parser.parse_program()
    env: Environment = Environment()
    if len(parser.errors) > 0:
        _print_parse_errors(parser.errors)
        return

    evaluated = evaluate(program,env)
    #assert evaluated is not None
    if type(evaluated) == Error:
        print(evaluated.inspect())

#Cuando se use la consola poder ejecutar codigo hasta que se utilize salir()
def loop_evaluator() -> None:
    #Si solo se quiere usar el evaluador sin archivo
    #TODO: si se dectecta un error, no incluir la linea en el scanned
    scanned: List[str] = []
    while (source := input('-> ')) != 'salir()':
        star_repl(source,scanned)
    
#Con la ruta al archivo, tomar el cotenido del archivo y pasarlo por el lexer o sino, salta un error
def file_evaluator(path:str) -> None:
    src = None
    scanned: List[str] = []
    try:
        with open(path, mode='r', encoding='utf-8') as file:
            lines = file.read()
        src = lines
        star_repl(src,scanned)
    except FileNotFoundError:
        print(_FILENOTFOUND.format(path)+'\n')