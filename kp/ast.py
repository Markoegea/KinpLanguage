from abc import(ABC,abstractmethod)
from typing import (List,Optional)
from kp.token import Token

#Clase abstracta que es la base para el resto de clases
class ASTNode(ABC):

    @abstractmethod
    def token_literal(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

#Clase Statement que hereda de ASTNode, recibe un token como parametro
class Statement(ASTNode):

    def __init__(self,token: Token) -> None:
        self.token = token
    
    def token_literal(self) -> str:
        return self.token.literal

#Clase Expression que hereda de ASTNode, recibe un token como parametro
class Expression(ASTNode):

    def __init__(self,token: Token) -> None:
        self.token = token
    
    def token_literal(self) -> str:
        return self.token.literal

#Clase Program que hereda de ASTNode, tiene como parametro una lista de Statements, que puede devolver
#Es la clase que contiene todos los statements parseados de nuestro programa
class Program(ASTNode):

    def __init__(self, statements: List[Statement])->None:
        self.statements = statements

    def token_literal(self)->str:
        if len(self.statements)>0:
            return self.statements[0].token_literal()
        return ''
    
    def __str__(self) -> str:
        out: List[str] =[]
        for statement in self.statements:
            out.append(str(statement))
        return ''.join(out)

#Clase Identifier que hereda de Expression, recibe como parametros un token y su valor
class Identifier(Expression):
    def __init__(self,
            token: Token,
            value: str) -> None:
        super().__init__(token)
        self.value = value

    def __str__(self)-> str:
        return self.value

#Clase Integer que hereda de Expression, recibe como parametros un token y su valor, que debe ser un entero
class Integer(Expression):
    def __init__(self,
            token: Token,
            value: Optional[int] = None) -> None:
        super().__init__(token)
        self.value = value
    
    def __str__(self)->str:
        return str(self.value)

#Clase Prefix que hereda de Expression, recibe como parametros un token, un operador y una expresion(Indentifier o Integer)
class Prefix(Expression):
    def __init__(self,
            token: Token,
            operator: str,
            right: Optional[Expression] = None) -> None:
        super().__init__(token)
        self.operator = operator
        self.right = right
    
    def __str__(self)->str:
        return f'({self.operator}{str(self.right)})'

#Clase LetStatement que hereda de Statement, 
#recibe como parametros un token, un identificador como nombre y Expresion como valor
#Esta guarda una declaracion de una variable, como pude ser, variable edad = 18;
class LetStatement(Statement):

    def __init__(self,
                token: Token,
                name: Optional[Identifier] = None,
                value: Optional[Expression] = None) -> None:
        super().__init__(token)
        self.name = name
        self.value = value
    
    def __str__(self)->str:
        return f'{self.token_literal()} {str(self.name)} = {str(self.value)};'

    def get_name(self)->str:
        return f'{str(self.name)}'

#Clase ReturnStatement que hereda de Statement, 
#recibe como parametros un token, Expresion como de retorno
#Esta guarda un retorno de una variable o de un tipo de dato, como pude ser, regresa verdadero;
class ReturnStatement(Statement):
    def __init__(self,
                token: Token,
                return_value: Optional[Expression] = None) -> None:
        super().__init__(token)
        self.return_value = return_value

    def __str__(self) -> str:
        return f'{self.token_literal()} {str(self.return_value)};'

#Clase ExpressionStatement que hereda de Statement, 
#recibe como parametros un token, Expresion como una expresion
#Esta guarda una expresion como pude ser, edad;
class ExpressionStatement(Statement):
    def __init__(self,
                token: Token,
                expression: Optional[Expression] = None) -> None:
        super().__init__(token)
        self.expression = expression
    
    def __str__(self) -> str:
        return str(self.expression)
