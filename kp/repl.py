from kp.lexer import Lexer
from kp.token import (
    Token,
    TokenType,
)

EOF_TOKEN: Token = Token(TokenType.EOF,'')

def star_repl() -> None:
    while (source := input('-> ')) != 'salir()':
        lexer: Lexer = Lexer(source)
        while (token := lexer.next_token()) != EOF_TOKEN:
            print(token)