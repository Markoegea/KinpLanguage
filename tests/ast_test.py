from unittest import TestCase

from kp.token import(
    Token,
    TokenType,
)
from kp.ast import (
    Program,
    Integer,
    Identifier,
    Expression,
    LetStatement,
    ReturnStatement,
    ExpressionStatement)

class ASTTest(TestCase):
    def test_let_statement(self) -> None:
        #Example: variable edad = 17;
        program: Program = Program(statements=[
            LetStatement(
                token=Token(TokenType.LET, literal='variable'),
                name=Identifier(
                    token=Token(TokenType.IDENT, literal='edad'),
                    value='edad'
                ),
                value=Integer(
                    token=Token(TokenType.INT, literal='17'),
                    value = 17
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

    def test_expression_statement(self) -> None:

        program: Program = Program(statements=[
            ExpressionStatement(

                token=Token(TokenType.IDENT, literal="foobar"),

                expression=Identifier(
                    token=Token(TokenType.IDENT, literal="foobar"),
                    value="foobar"
                )
            ),
            ExpressionStatement(
                token=Token(TokenType.INT, literal="5"),
                expression=Integer(
                    token=Token(TokenType.INT, literal="5"),
                    value=5
                )
            )
        ])
        program_str = str(program)
        self.assertEquals(program_str, "foobar5") 