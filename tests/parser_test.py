from unittest import TestCase
from typing import (List,cast,Any,Type,Tuple)

from kp.token import(
    Token,
    TokenType,
)
from kp.ast import (
    If,
    Call,
    Block,
    Infix,
    Prefix,
    Boolean,
    Program,
    Integer,
    Function,
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

    def test_prefix_expression(self) -> None:
        source: str = '!5; -15; !verdadero;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        self._test_program_statements(parser,program,3)

        for statement,(expected_operator, expected_value) in zip(program.statements,[('!',5),('-',15),('!', True)]):
            statement = cast(ExpressionStatement,statement)
            self.assertIsInstance(statement.expression, Prefix)

            prefix = cast(Prefix,statement.expression)
            
            self.assertEquals(prefix.operator, expected_operator)

            assert prefix.right is not None
            self._test_literal_expression(prefix.right,expected_value)

    def test_infix_expressions(self)-> None:
        source: str = '''
        5 + 5;
        5 - 5;
        5 * 5;
        5 / 5;
        5 > 5;
        5 < 5;
        5 == 5;
        5 != 5;
        verdadero == verdadero;
        verdadero != falso;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        self._test_program_statements(parser,program,expected_statements_count=10)
        expected_operators_and_values: List[Tuple[Any,str,Any]] = [
            (5,'+',5),
            (5,'-',5),
            (5,'*',5),
            (5,'/',5),
            (5,'>',5),
            (5,'<',5),
            (5,'==',5),
            (5,'!=',5),
            (True, '==', True),
            (True, '!=', False),
        ]
        for statement, (expected_left, expected_operator, expected_right) in zip(program.statements,expected_operators_and_values):
            statement = cast(ExpressionStatement, statement)
            assert statement.expression is not None
            self.assertIsInstance(statement.expression, Infix)
            self._test_infix_expression(statement.expression,expected_left,expected_operator,expected_right)

    def test_boolean_expression(self)->None:
        source: str = '''
        verdadero; falso;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        self._test_program_statements(parser,program,expected_statements_count=2)

        expected_values: List[bool] = [True, False]

        for statement,expected_value in zip(program.statements,expected_values):
            expression_statement = cast(ExpressionStatement,statement)
            assert expression_statement.expression is not None
            self._test_literal_expression(expression_statement.expression,expected_value)
        
    def test_operator_precedence(self)->None:
        test_sources: List[Tuple[str,str,int]] = [
            ('-a * b;', '((-a) * b)', 1),
            ('!-a;', '(!(-a))',1),
            ('a + b / c;', '(a + (b / c))',1),
            ('3 + 4; -5 * 5;','(3 + 4)((-5) * 5)',2),
            ('15+20/290+15*2;','((15 + (20 / 290)) + (15 * 2))',1),
            ('15+(((20/290)*15)*2)-100+(11*23);','(((15 + (((20 / 290) * 15) * 2)) - 100) + (11 * 23))',1),
            ('1 + (2 + 3) + 4;' , '((1 + (2 + 3)) + 4)',1),
            ('(5 + 5) * 2;' , '((5 + 5) * 2)',1),
            ('(2 / (5 + 5));' , '(2 / (5 + 5))',1),
            ('-(5 + 5);' , '(-(5 + 5))',1),
            ('(5 > 2) == ((18 < 15));' , '((5 > 2) == (18 < 15))',1),
            ('a+ suma(b*c)+d;', '((a + suma((b * c))) + d)',1),
            ('suma(a, b, 1, 2 * 3, 4+5, suma(6,7*8));', 'suma(a, b, 1, (2 * 3), (4 + 5), suma(6, (7 * 8)))',1),
            ('suma(a + b + c * d / f + g);', 'suma((((a + b) + ((c * d) / f)) + g))',1),
        ]
        for source, expected_result, expected_statements_count in test_sources:
            lexer: Lexer = Lexer(source)
            parser: Parser = Parser(lexer)
            program: Program = parser.parse_program()
            self._test_program_statements(parser,program,expected_statements_count)
            self.assertEquals(str(program),expected_result)

    def test_if_expression(self) -> None:
            source: str = 'si (x < y) { z }'
            lexer: Lexer = Lexer(source) 
            parser: Parser = Parser(lexer)
            program: Program = parser.parse_program()
            self._test_program_statements(parser,program)

            #Test correct node type
            if_expresion = cast(If, cast(ExpressionStatement, program.statements[0]).expression)
            self.assertIsInstance(if_expresion, If)

            #Test condition
            assert if_expresion.condition is not None
            self._test_infix_expression(if_expresion.condition, 'x','<', 'y')

            #Test consecuence
            assert if_expresion.consecuence is not None
            self.assertIsInstance(if_expresion.consecuence, Block)
            self.assertEquals(len(if_expresion.consecuence.statements),1)
            
            consecuence_statement = cast(ExpressionStatement, if_expresion.consecuence.statements[0])
            assert consecuence_statement.expression is not None
            self._test_identifier(consecuence_statement.expression, 'z')

            #Test alternative
            self.assertIsNone(if_expresion.alternative)

    def test_if_else_expression(self) -> None:
            source: str = '''
            si (x == 5) { 
                regresa verdadero; 
            } si_no {
                z 
            }
            '''
            lexer: Lexer = Lexer(source) 
            parser: Parser = Parser(lexer)
            program: Program = parser.parse_program()
            #print(str(program))
            self._test_program_statements(parser,program,1)
            if_expresion = cast(If, cast(ExpressionStatement, program.statements[0]).expression)
            self.assertIsInstance(if_expresion, If)

            #Test condition
            assert if_expresion.condition is not None
            self._test_infix_expression(if_expresion.condition, 'x','==', 5)

            #Test consecuence
            assert if_expresion.consecuence is not None
            self.assertIsInstance(if_expresion.consecuence, Block)
            self.assertEquals(len(if_expresion.consecuence.statements),1)
            
            #TODO: Cuando sepa parsear expresiones
            #consecuence_statement = cast(ReturnStatement, if_expresion.consecuence.statements[0])
            #assert consecuence_statement.return_value is not None
            #self._test_literal_expression(consecuence_statement.return_value, True)

            #Test alternative
            assert if_expresion.alternative is not None
            self.assertIsInstance(if_expresion.alternative, Block)
            self.assertEquals(len(if_expresion.alternative.statements),1)
            
            alternative_statement = cast(ExpressionStatement, if_expresion.alternative.statements[0])
            assert alternative_statement.expression is not None
            self._test_identifier(alternative_statement.expression, 'z')

    def test_function_literal(self) -> None:
        source: str = 'procedimiento(x,y) { x + y}'
        lexer: Lexer = Lexer(source) 
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        # Test correct node type
        function_literal = cast(Function, cast(ExpressionStatement, program.statements[0]).expression)

        self.assertIsInstance(function_literal, Function)

        #Test params
        self.assertEquals(len(function_literal.parameters), 2)
        self._test_literal_expression(function_literal.parameters[0], 'x')
        self._test_literal_expression(function_literal.parameters[1], 'y')

        #Test body
        assert function_literal.body is not None
        self.assertEquals(len(function_literal.body.statements),1)
        body = cast(ExpressionStatement, function_literal.body.statements[0])
        assert body.expression is not None
        self._test_infix_expression(body.expression, 'x', '+', 'y')

    def test_function_parameters(self)-> None:
        tests = [
            {'input':'procedimiento() {};',
            'expected_params': []},
            {'input':'procedimiento(x) {};',
            'expected_params': ['x']},
            {'input':'procedimiento(x,y,z) {};',
            'expected_params': ['x','y','z']},
        ]

        for test in tests:
            lexer: Lexer = Lexer(test['input']) # type: ignore
            parser: Parser = Parser(lexer)
            program: Program = parser.parse_program()

            function = cast(Function, cast(ExpressionStatement,program.statements[0]).expression)
            self.assertEquals(len(function.parameters), len(test['expected_params']))

            for idx, param in enumerate(test['expected_params']):
                self._test_literal_expression(function.parameters[idx], param)

    def test_call_expression(self) -> None:
        source: str = 'suma(1, 2 * 3, 4 + 5);'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        call = cast(Call, cast(ExpressionStatement,program.statements[0]).expression)

        self.assertIsInstance(call, Call)
        self._test_identifier(call.function, 'suma')

        #Test arguments
        assert call.arguments is not None
        self.assertEquals(len(call.arguments), 3)
        self._test_literal_expression(call.arguments[0], 1)
        self._test_infix_expression(call.arguments[1], 2, '*', 3)
        self._test_infix_expression(call.arguments[2], 4, '+', 5)

#######################AUXILIAR FUNCTIONS###########################################
    def _test_infix_expression(self, expression: Expression,
                                expected_left: Any,
                                expected_operator:str,
                                expected_right: Any):
        infix = cast(Infix,expression)
        assert infix.left is not None
        self._test_literal_expression(infix.left, expected_left)

        self.assertEquals(infix.operator,expected_operator)

        assert infix.right is not None
        self._test_literal_expression(infix.right, expected_right)

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
        elif value_type == bool:
            self._test_boolean(expression,expected_value)
        else:
            self.fail(f'Unhandled type of expression. Got={value_type}')

    def _test_boolean(self,
                        expression: Expression,
                        expected_value:bool)-> None:
        self.assertIsInstance(expression, Boolean)

        boolean = cast(Boolean, expression)
        
        self.assertEquals(boolean.value, expected_value)
        self.assertEquals(boolean.token.literal, 'verdadero' if expected_value else 'falso') 

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

        