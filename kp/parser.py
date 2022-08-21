from enum import IntEnum
from typing import (Callable,Dict,Optional,List)

from kp.ast import (
    Prefix,
    Program,
    Integer,
    Identifier,
    Expression,
    Statement,
    LetStatement,
    ReturnStatement,
    ExpressionStatement,
)
from kp.lexer import Lexer
from kp.token import(
    Token,
    TokenType,
)

#Parametros globales
#Son funciones que pueden ser llamasdas, con sus respectivos parametros y valores de retorno
PrefixParseFn = Callable[[], Optional [Expression]]
InfixParseFn = Callable[[Expression], Optional [Expression]]
#Son Diccionarios que tienen como llaven un tipo de Token y como su valor, una de las funciones antes mencionadas
PrefixParseFns = Dict[TokenType, PrefixParseFn]
InfixParseFns = Dict[TokenType, InfixParseFn]

#Enum que contine la precedencia o el orden de las expresiones que se parsean
class Precedence(IntEnum):
    LOWEST = 1
    EQUALS = 2
    LESSGREATER = 3
    SUM = 4
    PRODUCT = 5
    PREFIX = 6
    CALL = 7

#Clase parser, que se encarga de parsear todos los token que manda el lexer
class Parser:

    #Se definen los variables
    def __init__(self, lexer: Lexer) -> None:
        self._lexer = lexer
        self._current_token: Optional[Token] = None
        self._peek_token: Optional[Token] = None
        self._errors: List[str]=[]

        self._prefix_parse_fns: PrefixParseFns = self._register_prefix_fns()
        self._infix_parse_fns: InfixParseFns = self._register_infix_fns()

        self._advance_tokens()
        self._advance_tokens()

    #Funcion con decorador, para especificar que es funcion pra obtener una variable de la clase
    @property
    def errors(self) -> List[str]:
        return self._errors

    #Funcion que inicia el parseo, al establecer un ciclo que se encarga de que recorra todos los tokens de nuestro programa
    #Hasta que se terminen y si son statements validos, los añade a lista de la clase Program del ast.py
    def parse_program(self) -> Program:
        program: Program = Program(statements=[])

        assert self._current_token is not None
        while self._current_token.token_type != TokenType.EOF:
            statement = self._parse_statement()
            if statement is not None:
                #Si es valido el statement, se añade a la lista de Program
                program.statements.append(statement)
            self._advance_tokens()

        return program

    #Funcion para avanzar tokens
    def _advance_tokens(self)->None:
        self._current_token = self._peek_token
        self._peek_token = self._lexer.next_token()

    #Funcion para comprobar si el token que sigue es el correcto
    def _expected_token(self, token_type: TokenType) -> bool:
        assert self._peek_token is not None
        if self._peek_token.token_type == token_type:
            self._advance_tokens()
            return True
        self._expected_token_error(token_type)
        return False
    
    #De ser el token siguente incorrecto, se agrega a la lista de errores
    def _expected_token_error(self, token_type:TokenType)->None:
        assert self._peek_token is not None
        error = f'Se esperaba que el siguente token fuera {token_type} ' + \
                f'Pero se obtuvo {self._peek_token.token_type}'
        self._errors.append(error)

    #Con esta funcion, devolvemos una expresion dependiendo de con cual token nos encontremos
    def _parse_expresion(self, precedence: Precedence) -> Optional[Expression]:
        assert self._current_token is not None
        try:
            #Intenta acceder al diccionario de prefix, utilizando el token actual como llave
            prefix_parse_fn = self._prefix_parse_fns[self._current_token.token_type]
        except KeyError:
            #Si no encuentra ninguna coincidencia, significa que hubo un error y emite un error
            message = f'No se encontro ninguna funcion para parsear {self._current_token.literal}'
            self._errors.append(message)
            return None
        
        #Si todo sale bien, ejecuta la funcion correspondiente al prefix encontrado
        left_expression = prefix_parse_fn()
        # Y devuelve la expresion resultante
        return left_expression

    #Si el token no es ni let, ni return, significa que es una expresion y entra a esta funcion
    def _parse_expression_statements(self) -> Optional[ExpressionStatement]:
        assert self._current_token is not None
        #Se crea un instancia de la clase ExpressionStatement, con el token actual
        expression_statement = ExpressionStatement(token=self._current_token)
        #Para agregar el parametro expression a la clase, necesitamos crear una Expresion, con una precedencia
        expression_statement.expression = self._parse_expresion(Precedence.LOWEST)

        assert self._peek_token is not None
        if self._peek_token.token_type == TokenType.SEMICOLON:
            self._advance_tokens()

        return expression_statement

    #Parsea el token actual como un tipo Identifier
    def _parse_identifier(self)->Identifier:
        assert self._current_token is not None

        return Identifier(token=self._current_token,
                        value=self._current_token.literal)

    #Parsea el token actual como un tipo Integer
    def _parse_integer(self)-> Optional[Integer]:
        assert self._current_token is not None
        integer = Integer(token=self._current_token)
        try:
            integer.value = int(self._current_token.literal)
        except ValueError:
            #Si el valor del token no es un numero, agrega el error a la lista de errores
            message = f'No se ha podido parsear {self._current_token.literal} como entero'
            self._errors.append(message)
            return None

        return integer

    #Parsea el token actual como un tipo Prefix
    def _parse_prefix_expresion(self)->Prefix:
        assert self._current_token is not None
        #Crea la instancia en la clase Prefix con el token actual
        prefix_expression = Prefix(token=self._current_token,operator=self._current_token.literal)
        self._advance_tokens()
        #Pero para obtener la variable right de Prefix, necesitamos un expresion
        prefix_expression.right =   self._parse_expresion(Precedence.PREFIX)
        
        return prefix_expression
 
    #Si el token resulta ser un tipo Let, significa que estamos declarando un variable y entra aqui
    def _parse_let_statement(self)-> Optional[LetStatement]:
        assert self._current_token is not None
        #Inicializamos un instancia LetStatement, con el token actual
        let_statement = LetStatement(token=self._current_token)

        if not self._expected_token(TokenType.IDENT):
            return None

        #la variable name del LetStatement, es un identifier que retorna de otra funcion
        let_statement.name = self._parse_identifier()

        if not self._expected_token(TokenType.ASSIGN):
            return None

        #TODO terminar cuando sepamos parsear expresiones

        #Avanza hasta que encuentre un punto y coma, o el final del archivo
        while self._current_token.token_type != TokenType.SEMICOLON and self._current_token.token_type != TokenType.EOF:
            self._advance_tokens()
        #Por ultimo retorna el LetStatement
        return let_statement

    #Si el token resulta ser un tipo Return, significa que estamos retornando una expresion
    def _parse_return_statement(self) -> Optional[ReturnStatement]:
        assert self._current_token is not None
        #Inicializamos un instancia ReturnStatement, con el token actual
        return_statement = ReturnStatement(token=self._current_token)

        self._advance_tokens()

        # TODO terminar cuando sepamos parsear expresiones
        #Avanza hasta que encuentre un punto y coma, o el final del archivo
        while self._current_token.token_type != TokenType.SEMICOLON and self._current_token.token_type != TokenType.EOF:
            self._advance_tokens()
        #Por ultimo retorna el ReturnStatement
        return return_statement
    
    #Cuando pasa un token, revisa que tipo de token es, de esta manera entra a una funcion
    def _parse_statement(self) -> Optional[Statement]:
            assert self._current_token is not None
            if self._current_token.token_type == TokenType.LET:
                return self._parse_let_statement()
            elif self._current_token.token_type == TokenType.RETURN:
                return self._parse_return_statement()
            else:
                return self._parse_expression_statements()

    #Un diccionario con todos los tipos de infix y su funcion de parseo
    def _register_infix_fns(self) -> InfixParseFns:
        return {}
    #Un diccionario con todos los tipos de prefix y su funcion de parseo
    def _register_prefix_fns(self) -> PrefixParseFns:
        return {
            TokenType.IDENT : self._parse_identifier,
            TokenType.INT: self._parse_integer,
            TokenType.LESS: self._parse_prefix_expresion,
            TokenType.NEGATION: self._parse_prefix_expresion,
        }