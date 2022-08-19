from unittest import TestCase

from kp.token import(
    Token,
    TokenType,
)
from kp.ast import (
    Program,
    Identifier,
    Expression,
    LetStatement,
    ReturnStatement)

class ASTTest(TestCase):
    def test_let_statement(self) -> None:
        #Example: variable edad = 17;
        #TODO: Si se agrega una expresion de numeros, modificar aqui
        program: Program = Program(statements=[
            LetStatement(
                token=Token(TokenType.LET, literal='variable'),
                name=Identifier(
                    token=Token(TokenType.IDENT, literal='edad'),
                    value='edad'
                ),
                value=Identifier(
                    token=Token(TokenType.INT, literal='17'),
                    value = '17'
                ),
            )
        ])
        program_str = str(program)

        self.assertEquals(program_str, 'variable edad = 17;')
    
    def test_return_statament(self)-> None:
        #Example: regresa edad;
        program: Program = Program(statements=[
            ReturnStatement(
                token=Token(TokenType.RETURN, literal='regresa'),
                return_value=Identifier(
                    token=Token(TokenType.IDENT, literal='edad'),
                    value='edad'
                )
            )
        ])

        program_str = str(program)

        self.assertEquals(program_str, 'regresa edad;')