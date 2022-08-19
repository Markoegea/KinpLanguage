from unittest import TestCase
from typing import (List,cast,Any,Type)

from kp.token import(
    Token,
    TokenType,
)
from kp.ast import (
    Prefix,
    Program,
    Integer,
    Identifier,
    Expression,
    LetStatement,
    ReturnStatement,
    ExpressionStatement
)
from kp.lexer import Lexer
from kp.parser import Parser

class ParserTest(TestCase):

    def test_parse_program(self)->None:
        source: str = 'variable x =5;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertIsNotNone(program)
        self.assertIsInstance(program,Program)
    
    def test_let_statement(self)->None:
        source: str = '''
            variable x = 5;
            variable y = 10;
            variable foo = 20;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        self.assertEqual(len(program.statements),3)

        for statement in program.statements:
            self.assertEqual(statement.token_literal(), 'variable')
            self.assertIsInstance(statement, LetStatement)

    def test_names_let_statement(self) -> None: 
        source: str = '''
            variable x = 5;
            variable y = 10;
            variable foo = 20;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        expected_statements: List[str] = [
            'x','y','foo'
        ]
        statements: List[str] = []

        for statement in program.statements:
            let_statement = cast(LetStatement,statement)
            assert let_statement.name is not None
            statements.append(let_statement.name.value)

        self.assertEquals(statements, expected_statements)
    
    def test_parse_errors(self) -> None:
        source:  str = 'variable x 5;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()
        print(parser.errors)

        self.assertEqual(len(parser.errors),1)

    def test_return_statament(self) -> None:
        source: str = '''
            regresa 5;
            regresa foo;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        self.assertEquals(len(program.statements),2)
        for statement in program.statements:
            self.assertEquals(statement.token_literal(), 'regresa')
            self.assertIsInstance(statement, ReturnStatement)
    
    def test_identifier_expression(self) -> None:
        source: str = 'foobar;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        expression_statement = cast(ExpressionStatement, program.statements[0])

        assert expression_statement.expression is not None
        self._test_literal_expression(expression_statement.expression, 'foobar')

    def test_integer_expressions(self)-> None:
        source: str = '5;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        self._test_program_statements(parser,program)

        expression_statement = cast(ExpressionStatement, program.statements[0])
        assert expression_statement.expression is not None
        self._test_literal_expression(expression_statement.expression,5)

    def _test_prefix_expression(self)-> None:
        source: str = '!5; -15;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        self._test_program_statements(parser,program,expected_statements_count=2)

        # for statement,(expected_operator, expected_value) in zip(program.statements,[('!',5),('-',15)]):
        #     statement = cast(ExpressionStatement,statement)
        #     self.assertIsInstance(statement.expression, Prefix)
        #     prefix = cast(Prefix,statement.expression)
        #     self.assertEquals(prefix.operator, expected_operator)
        #     assert prefix.right is not None
        #     self._test_literal_expression(prefix.right,expected_value)

    def _test_program_statements(self,
                                    parser: Parser,
                                    program: Program,
                                    expected_statements_count: int = 1) -> None:
        if parser.errors:
            print(parser.errors)
            
        self.assertEquals(len(parser.errors),0)
        self.assertEquals(len(program.statements), expected_statements_count)
        self.assertIsInstance(program.statements[0], ExpressionStatement)

    def _test_literal_expression(self,
                                    expression: Expression,
                                    expected_value: Any) -> None:
        value_type: Type = type(expected_value)

        if value_type == str:
            self._test_identifier(expression,expected_value)
        elif value_type == int:
            self._test_integer(expression,expected_value)
        else:
            self.fail(f'Unhandled type of expression. Got={value_type}')

    def _test_identifier(self,
                        expression: Expression,
                        expected_value:str)-> None:
        self.assertIsInstance(expression, Identifier)

        identifier = cast(Identifier, expression)
        
        self.assertEquals(identifier.value, expected_value)
        self.assertEquals(identifier.token.literal, expected_value)
    
    def _test_integer(self,
                        expression: Expression,
                        expected_value:int)-> None:
        self.assertIsInstance(expression,Integer)

        integer = cast(Integer, expression)
        self.assertEquals(integer.value, expected_value)
        self.assertEquals(integer.token.literal, str(expected_value))

        