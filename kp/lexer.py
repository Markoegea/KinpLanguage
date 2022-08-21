from re import match

from kp.token import(
    lookup_token_type,
    Token,
    TokenType,
)
#El Lexer es el encargado de sacar los token del la cade de string que le envio
class Lexer:
    #Defino los parametros que va a tener el lexer
    #La cadena de string que yo escribo
    #Un caracter individual de ese string
    #Una posicion dentro de la cadena de string
    #Otra posicion dentro de la cadena de string, que por lo general esta atras de la anterior
    def __init__(self,source:str)->None:
        #TODO: Crear otro variable para poder colocar la posicion siguente a self._read_position,
        # para asi tener infix operators de tres caracteres
        self._source: str = source
        self._character: str = ''
        self._read_position : int = 0
        self._position: int = 0
        
        #Leo los caracteres para darle a la variable self._character el primer caracter de la cadena 
        # Y poner la variable self._position en la posicion cero y la variable self._read_position en la posicion 1
        # Para de esta manera tener la posicion del caracter actual y la del siguente
        self._read_character()
    
    #La funcion principal del lexer, que es ir caracter por caracter y dependiendo del caracter crearme un token
    def next_token(self)->Token:
        #Funcion para saltarse los espacios en blanco
        self._skip_whitespace()

        if match(r'^\=$', self._character):
            if self._peek_character() == '=':
                token = self._make_two_character_token(TokenType.EQ)
            else:
                token = Token(TokenType.ASSIGN, self._character)

        elif match(r'^\-$', self._character):
            token = Token(TokenType.LESS, self._character)

        elif match(r'^\/$', self._character):
            token = Token(TokenType.DIVISION, self._character)

        elif match(r'^\+$', self._character):
            token = Token(TokenType.PLUS, self._character)

        elif match(r'^\*$', self._character):
            token = Token(TokenType.MULTIPLICATION, self._character)

        elif match(r'^$',self._character):
            token = Token(TokenType.EOF, self._character)

        elif match(r'^\($',self._character):
            token = Token(TokenType.LPAREN, self._character)

        elif match(r'^\)$',self._character):
            token = Token(TokenType.RPAREN, self._character)

        elif match(r'^\{$',self._character):
            token = Token(TokenType.LBRACE, self._character)

        elif match(r'^\}$',self._character):
            token = Token(TokenType.RBRACE, self._character)

        elif match(r'^\,$',self._character):
            token = Token(TokenType.COMMA, self._character)

        elif match(r'^\;$',self._character):
            token = Token(TokenType.SEMICOLON, self._character)
        
        elif match(r'^\<$',self._character):
            token = Token(TokenType.LT, self._character)

        elif match(r'^\>$',self._character):
            token = Token(TokenType.GT, self._character)

        elif match(r'^!$',self._character):
            if self._peek_character() == '=':
                token = self._make_two_character_token(TokenType.NOT_EQ)
            else:
                token = Token(TokenType.NEGATION, self._character)

        elif self._is_letter(self._character):
            literal = self._read_identifier()
            token_type = lookup_token_type(literal)
            return Token(token_type, literal)

        elif self._is_number(self._character):
            literal = self._read_number()
            return Token(TokenType.INT, literal)

        else:
            token = Token(TokenType.ILLEGAL, self._character)

        self._read_character()
        return token

    #Funcion para saber si estoy frente a una letra
    def _is_letter(self, character:str) -> bool:
        return bool(match(r'^[a-záéíóúA-ZÁÉÍÓÚñÑ_]$',character))

    #Funcion para saber si estoy frente a un numero
    def _is_number(self, character:str) -> bool:
        return bool(match(r'^\d$', character))
    
    #Funcion la cual me regresa un token de dos caracteres
    def _make_two_character_token(self, token_type: TokenType)-> Token:
        prefix = self._character
        self._read_character()
        suffix = self._character
        return Token(token_type,f'{prefix}{suffix}')

    #Funcion para moverme entre los caracteres del string de entrada
    def _read_character(self) -> None:
        if self._read_position >= len(self._source):
            self._character = ''
        else:
            self._character = self._source[self._read_position]
        
        self._position = self._read_position
        self._read_position +=1

    #Funcion que es llamada cuando se detecta una letra, para devolver toda la palabra 
    def _read_identifier(self) -> str:
        initial_position = self._position

        while self._is_letter(self._character) or self._is_number(self._character):
            self._read_character()
        
        return self._source[initial_position:self._position]

    #Funcion que es llamada cuando se detecta un numero, para devolver toda el numero
    def _read_number(self) -> str:
        initial_position = self._position

        while self._is_number(self._character):
            self._read_character()

        return self._source[initial_position:self._position]
    
    #Funcion que me devuelve el string siguente para comprobar si es un operador de mas de un caracter
    def _peek_character(self)->str:
        if self._read_position >= len(self._source):
            return ''
        return self._source[self._read_position]

    #Funcion que me salta los espacios vacios, pues no me representan nada
    def _skip_whitespace(self)->None:
        while match(r'^\s$', self._character):
            self._read_character()