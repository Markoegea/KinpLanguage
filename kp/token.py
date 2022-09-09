from enum import (auto,Enum,unique)
from typing import (Dict,NamedTuple)

#Enum donde se colocan todos los nombres de los token que pueden haber en el lenguaje
@unique
class TokenType(Enum):
    ASSIGN = auto(),
    COMMA = auto(),
    DIVISION = auto(),
    ELSE = auto(),
    EOF = auto(),
    EQ = auto(),
    FALSE = auto(),
    FLOAT = auto(),
    FUNCTION = auto(),
    IDENT = auto(),
    IF = auto(),
    ILLEGAL = auto(),
    INT = auto(),
    LBRACE = auto(),
    LESS = auto(),
    LET = auto(),
    LPAREN = auto(),
    LT = auto(),
    LEQT = auto(),
    GT = auto(),
    GEQT = auto(),
    MULTIPLICATION = auto(),
    MOD = auto(),
    NEGATION = auto(),
    NOT_EQ = auto(),
    PLUS = auto(),
    RBRACE = auto(),
    RETURN = auto(),
    RTP = auto(),
    RPAREN = auto(),
    SEMICOLON = auto(),
    STRING = auto()
    TRUE = auto(),

#Una clase donde se crean los token, que tiene como parametros el nombre del token(enum) y el valor de ese token
class Token(NamedTuple):
    token_type : TokenType
    literal: str

    def __str__(self) -> str:
        return f'Type: {self.token_type}, Literal: {self.literal}'

#Funcion que contiene las palabras reservadas del lenguaje, si el dado caso no es ninguna es un dato identificador
def lookup_token_type(literal:str) -> TokenType:
    keywords: Dict[str, TokenType] = {
        'falso': TokenType.FALSE,
        'procedimiento': TokenType.FUNCTION,
        'regresa': TokenType.RETURN,
        'si' : TokenType.IF,
        'si_no': TokenType.ELSE,
        'variable': TokenType.LET,
        'verdadero': TokenType.TRUE,
    }

    return keywords.get(literal, TokenType.IDENT)