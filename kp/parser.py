from enum import IntEnum
from typing import (Callable,Dict,Optional,List)

from kp.ast import (
    If,
    Call,
    Null,
    Float,
    Block,
    Infix,
    Prefix,
    Boolean,
    Program,
    Integer,
    Function,
    Identifier,
    Expression,
    Statement,
    LetStatement,
    StringLiteral,
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
    RAISE = 6
    PREFIX = 7
    CALL = 8

PRECEDENCES: Dict[TokenType,Precedence] = {
    TokenType.ASSIGN: Precedence.EQUALS,
    TokenType.EQ: Precedence.EQUALS,
    TokenType.NOT_EQ: Precedence.EQUALS,
    TokenType.LT: Precedence.LESSGREATER,
    TokenType.LEQT: Precedence.LESSGREATER,
    TokenType.GT: Precedence.LESSGREATER,
    TokenType.GEQT: Precedence.LESSGREATER,
    TokenType.PLUS: Precedence.SUM,
    TokenType.LESS: Precedence.SUM,
    TokenType.DIVISION: Precedence.PRODUCT,
    TokenType.MULTIPLICATION: Precedence.PRODUCT,
    TokenType.MOD: Precedence.PRODUCT,
    TokenType.LPAREN: Precedence.CALL,
    TokenType.RTP: Precedence.RAISE,
}

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

    #Funcion para obtener la precedencia del token actual
    def _current_precedence(self) -> Precedence:
        assert self._current_token is not None
        try:
            return PRECEDENCES[self._current_token.token_type]
        except KeyError:
            return Precedence.LOWEST

    #Funcion para comprobar si el token que sigue es el correcto
    def _expected_token(self, token: Token) -> bool:
        assert self._peek_token is not None
        if self._peek_token.token_type == token.token_type:
            self._advance_tokens()
            return True
        self._expected_token_error(token)
        return False

    #Funcion para comprobar si el token que ahi es el correcto
    def _current_correct_token(self, token: Token) -> bool:
        assert self._current_token is not None
        if self._current_token.token_type == token.token_type:
            return True
        self._expected_token_error(token)
        return False
    
    #De ser el token siguente incorrecto, se agrega a la lista de errores
    def _expected_token_error(self, token:Token)->None:
        assert self._peek_token is not None
        error = f'Se esperaba un "{token.literal}" ' + \
                f'Pero se obtuvo un "{self._peek_token.literal}"'
        self._errors.append(error)

    #Con esta funcion, devolvemos una expresion dependiendo de con cual token nos encontremos
    def _parse_expresion(self, precedence: Precedence) -> Optional[Expression]:
        assert self._current_token is not None
        try:
            #Intenta acceder al diccionario de prefix, utilizando el token actual como llave
            prefix_parse_fn = self._prefix_parse_fns[self._current_token.token_type]
        except KeyError:
            #Si no encuentra ninguna coincidencia, significa que hubo un error y emite un error
            message = f'No se encontro ninguna funcion para parsear "{self._current_token.literal}"'
            self._errors.append(message)
            return None
        #Si todo sale bien, ejecuta la funcion correspondiente a la expresion encontrada
        left_expression = prefix_parse_fn()
        assert self._peek_token is not None
        while not self._peek_token.token_type == TokenType.SEMICOLON and precedence < self._peek_precedence():
            try:
                infix_parse_fn = self._infix_parse_fns[self._peek_token.token_type]
                self._advance_tokens()
                assert left_expression is not None
                left_expression = infix_parse_fn(left_expression)
            except KeyError:
                return left_expression
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

    def _parse_call(self, function: Expression) -> Call:
        assert self._current_token is not None
        call = Call(self._current_token,function)
        call.arguments = self._parse_call_arguments()
        return call

    def _parse_call_arguments(self) -> Optional[List[Expression]]:
        arguments: List[Expression] = []

        assert self._peek_token is not None
        if self._peek_token.token_type == TokenType.RPAREN:
            self._advance_tokens()
            return arguments
        self._advance_tokens()
        if expression:= self._parse_expresion(Precedence.LOWEST):
            arguments.append(expression)
        
        while self._peek_token.token_type == TokenType.COMMA:
            self._advance_tokens()
            self._advance_tokens()

            if expression:= self._parse_expresion(Precedence.LOWEST):
                arguments.append(expression)
        if not self._expected_token(Token(TokenType.RPAREN,')')):
            return None
        return arguments


    def _parse_function(self) -> Optional[Function]:
        assert self._current_token is not None
        function = Function(token=self._current_token)

        if not self._expected_token(Token(TokenType.LPAREN,'(')):
            return None

        function.parameters = self._parse_function_parameters()

        if not self._expected_token(Token(TokenType.LBRACE,'{')):
            return None
        
        function.body = self._parse_block()

        if not self._current_correct_token(Token(TokenType.RBRACE,'}')):
            return None

        return function

    def _parse_function_parameters(self) -> List[Identifier]:
        params: List[Identifier] = []
        assert self._peek_token is not None
        if self._peek_token.token_type == TokenType.RPAREN:
            self._advance_tokens()
            return params
        self._advance_tokens()
        identifier = self._parse_identifier()
        params.append(identifier)
        while self._peek_token.token_type == TokenType.COMMA:
            self._advance_tokens()
            self._advance_tokens()
            identifier = self._parse_identifier()
            params.append(identifier)
        if not self._expected_token(Token(TokenType.RPAREN, ')')):
            return []
        return params

    def _parse_grouped_expression(self) -> Optional[Expression]:
        self._advance_tokens()
        expression = self._parse_expresion(Precedence.LOWEST)
        if not self._expected_token(Token(TokenType.RPAREN,')')):
            return None
        return expression

    #Parsea el token actual como un tipo Boolean
    def _parse_boolean(self) -> Boolean:
        assert self._current_token is not None
        return Boolean(token= self._current_token,
                        value= self._current_token.token_type == TokenType.TRUE)

    #Parsea el token actual como un tipo Identifier
    def _parse_identifier(self)->Identifier:
        assert self._current_token is not None

        return Identifier(token=self._current_token,
                        value=self._current_token.literal)

    def _parse_string_literal(self) -> Expression:
        assert self._current_token is not None
        return StringLiteral(token=self._current_token,
                            value=self._current_token.literal)

    def _parse_block(self) -> Optional[Block]:
        assert self._current_token is not None
        block_statement = Block(token=self._current_token,
                                statements =[])
        self._advance_tokens()

        while not self._current_token.token_type == TokenType.RBRACE \
                    and not self._current_token.token_type == TokenType.EOF:
            statement = self._parse_statement()
            if statement:
                block_statement.statements.append(statement)
            self._advance_tokens()
        return block_statement

    def _parse_if(self) -> Optional[If]:
        assert self._current_token is not None
        if_expression = If(token=self._current_token)
        if not self._expected_token(Token(TokenType.LPAREN,'(')):
            return None
        self._advance_tokens()
        if_expression.condition = self._parse_expresion(Precedence.LOWEST)
        if not self._expected_token(Token(TokenType.RPAREN,')')):
            return None
        if not self._expected_token(Token(TokenType.LBRACE,'{')):
            return None
        if_expression.consecuence = self._parse_block()
        if not self._current_correct_token(Token(TokenType.RBRACE,'}')):
            return None

        assert self._peek_token is not None
        if self._peek_token.token_type == TokenType.ELSE:
            self._advance_tokens()
            if not self._expected_token(Token(TokenType.LBRACE,'{')):
                return None
            if_expression.alternative = self._parse_block()
            if not self._current_correct_token(Token(TokenType.RBRACE,'}')):
                return None
        return if_expression

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

    #Parsea el token actual como un tipo Float
    def _parse_float(self)-> Optional[Float]:
        assert self._current_token is not None
        floating = Float(token=self._current_token)
        try:
            floating.value = float(self._current_token.literal)
        except ValueError:
            #Si el valor del token no es un numero, agrega el error a la lista de errores
            message = f'No se ha podido parsear {self._current_token.literal} como entero'
            self._errors.append(message)
            return None

        return floating

    #Parsea el token actual como un tipo Infix, pero como este mismo tiene un lado derecho y uno izquierdo
    #Llama a la funcion self._parse_expresion, para traer esa expresion
    def _parse_infix_expression(self, left: Expression) -> Infix:
        assert self._current_token is not None
        infix = Infix(token=self._current_token,
                        operator=self._current_token.literal,
                        left=left)
        precedence = self._current_precedence()

        self._advance_tokens()

        infix.right = self._parse_expresion(precedence=precedence)

        return infix

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

        if not self._expected_token(Token(TokenType.IDENT,'nombre')):
            return None

        #la variable name del LetStatement, es un identifier que retorna de otra funcion
        let_statement.name = self._parse_identifier()

        assert self._peek_token is not None
        if self._peek_token.token_type != TokenType.SEMICOLON:

            if not self._expected_token(Token(TokenType.ASSIGN,'=')):
                return None

            self._advance_tokens()

            let_statement.value = self._parse_expresion(Precedence.LOWEST)
        else:
            let_statement.value = Null(self._current_token)


        if self._peek_token.token_type == TokenType.SEMICOLON:
            self._advance_tokens()

        return let_statement

    #Si el token resulta ser un tipo Return, significa que estamos retornando una expresion
    def _parse_return_statement(self) -> Optional[ReturnStatement]:
        assert self._current_token is not None
        #Inicializamos un instancia ReturnStatement, con el token actual
        return_statement = ReturnStatement(token=self._current_token)

        self._advance_tokens()

        assert self._peek_token is not None
        if self._current_token.token_type != TokenType.SEMICOLON:
            return_statement.return_value = self._parse_expresion(Precedence.LOWEST)
        else:
            return_statement.return_value = Null(self._current_token)

        if self._peek_token.token_type == TokenType.SEMICOLON:
            self._advance_tokens()

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
    
    #Funcion para obtener la precedencia del peek token
    def _peek_precedence(self)->Precedence:
        assert self._peek_token is not None
        try:
            return PRECEDENCES[self._peek_token.token_type]
        except KeyError:
            return Precedence.LOWEST

    #Un diccionario con todos los tipos de infix y su funcion de parseo
    def _register_infix_fns(self) -> InfixParseFns:
        return {
            TokenType.PLUS: self._parse_infix_expression,
            TokenType.LESS: self._parse_infix_expression,
            TokenType.DIVISION: self._parse_infix_expression,
            TokenType.MULTIPLICATION: self._parse_infix_expression,
            TokenType.MOD: self._parse_infix_expression,
            TokenType.EQ: self._parse_infix_expression,
            TokenType.NOT_EQ: self._parse_infix_expression,
            TokenType.LT: self._parse_infix_expression,
            TokenType.LEQT: self._parse_infix_expression,
            TokenType.GT: self._parse_infix_expression,
            TokenType.GEQT: self._parse_infix_expression,
            TokenType.RTP: self._parse_infix_expression,
            TokenType.LPAREN: self._parse_call,
            TokenType.ASSIGN: self._parse_infix_expression,
        }

    #Un diccionario con todos los tipos de prefix y su funcion de parseo
    def _register_prefix_fns(self) -> PrefixParseFns:
        return {
            TokenType.FALSE: self._parse_boolean,
            TokenType.FLOAT: self._parse_float,
            TokenType.FUNCTION: self._parse_function,
            TokenType.IDENT : self._parse_identifier,
            TokenType.IF: self._parse_if,
            TokenType.INT: self._parse_integer,
            TokenType.LPAREN: self._parse_grouped_expression,
            TokenType.LESS: self._parse_prefix_expresion,
            TokenType.NEGATION: self._parse_prefix_expresion,
            TokenType.TRUE: self._parse_boolean,
            TokenType.STRING: self._parse_string_literal,
        }