from unittest import TestCase
from typing import (List,cast,Any,Type,Tuple)

from kp.token import(
    Token,
    TokenType,
)
from kp.ast import (
    If,
    Call,
    Float,
    Block,
    Infix,
    Prefix,
    Lambda,
    Boolean,
    Program,
    Integer,
    Function,
    Identifier,
    Expression,
    LetStatement,
    StringLiteral,
    ReturnStatement,
    ExpressionStatement,
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
            /*variable pi = 3.14;*/
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

    def test_float_expressions(self)-> None:
        source: str = '89.576776575;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        self._test_program_statements(parser,program)

        expression_statement = cast(ExpressionStatement, program.statements[0])
        assert expression_statement.expression is not None
        self._test_literal_expression(expression_statement.expression,89.576776575)

    def test_prefix_expression(self) -> None:
        source: str = '!5; -15; !verdadero; -156.36;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        self._test_program_statements(parser,program,4)

        for statement,(expected_operator, expected_value) in zip(program.statements,[('!',5),('-',15),('!', True),('-', 156.36)]):
            statement = cast(ExpressionStatement,statement)
            self.assertIsInstance(statement.expression, Prefix)

            prefix = cast(Prefix,statement.expression)
            
            self.assertEquals(prefix.operator, expected_operator)

            assert prefix.right is not None
            self._test_literal_expression(prefix.right,expected_value)

    def test_infix_expressions(self)-> None:
        source: str = '''
        /*Number operations*/
        5 + 5;
        5 - 5;
        5 * 5;
        5 / 5;
        5 > 5;
        5 >= 5;
        5 < 5;
        5 <= 5;
        5 == 5;
        5 != 5;
        /*Bool operations*/
        verdadero == verdadero;
        verdadero != falso;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        self._test_program_statements(parser,program,expected_statements_count=12)
        expected_operators_and_values: List[Tuple[Any,str,Any]] = [
            (5,'+',5),
            (5,'-',5),
            (5,'*',5),
            (5,'/',5),
            (5,'>',5),
            (5,'>=',5),
            (5,'<',5),
            (5,'<=',5),
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

    def test_infix_float_expressions(self)-> None:
        source: str = '''
        5.1 + 5.2;
        5.3 - 5.4;
        5.45 * 5.52;
        5.64 / 5.73;
        5.9 > 5.86;
        5.11 >= 5.22;
        5.33 < 5.44;
        5.55 <= 5.66;
        5.77 == 5.88;
        5.1 != 5.1;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        self._test_program_statements(parser,program,expected_statements_count=10)
        expected_operators_and_values: List[Tuple[Any,str,Any]] = [
            (5.1,'+', 5.2),
            (5.3,'-',5.4),
            (5.45,'*',5.52),
            (5.64,'/',5.73),
            (5.90,'>',5.86),
            (5.11,'>=',5.22),
            (5.33,'<',5.44),
            (5.55,'<=',5.66),
            (5.77,'==',5.88),
            (5.1,'!=',5.1),
        ]
        for statement, (expected_left, expected_operator, expected_right) in zip(program.statements,expected_operators_and_values):
            statement = cast(ExpressionStatement, statement)
            assert statement.expression is not None
            self.assertIsInstance(statement.expression, Infix)
            self._test_infix_expression(statement.expression,expected_left,expected_operator,expected_right)

    def test_infix_raised_to_n_power(self)-> None:
        source: str = '''
        5 ** 5;
        15.55 ** 55.66;
        67 ** 89;
        0.111 ** 0.2;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        self._test_program_statements(parser,program,expected_statements_count=4)
        expected_operators_and_values: List[Tuple[Any,str,Any]] = [
            (5,'**', 5),
            (15.55,'**',55.66),
            (67,'**',89),
            (0.111,'**',0.2),
        ]
        for statement, (expected_left, expected_operator, expected_right) in zip(program.statements,expected_operators_and_values):
            statement = cast(ExpressionStatement, statement)
            assert statement.expression is not None
            self.assertIsInstance(statement.expression, Infix)
            self._test_infix_expression(statement.expression,expected_left,expected_operator,expected_right)

    def test_module_operation(self)-> None:
        source: str = '''
        5 % 5;
        15.55 % 55.66;
        67 % 89;
        0.111 % 0.2;
        90 % 9;
        24.75 % 32;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        self._test_program_statements(parser,program,expected_statements_count=6)
        expected_operators_and_values: List[Tuple[Any,str,Any]] = [
            (5,'%', 5),
            (15.55,'%',55.66),
            (67,'%',89),
            (0.111,'%',0.2),
            (90,'%',9),
            (24.75,'%',32),
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
                /*
                regresa verdadero
                */ 
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
            
            consecuence_statement = cast(ReturnStatement, if_expresion.consecuence.statements[0])
            assert consecuence_statement.return_value is not None
            self._test_literal_expression(consecuence_statement.return_value, True)

            #Test alternative
            assert if_expresion.alternative is not None
            self.assertIsInstance(if_expresion.alternative, Block)
            block_statement = cast(Block, if_expresion.alternative)
            self.assertEquals(len(block_statement.statements),1)
            
            alternative_statement = cast(ExpressionStatement, block_statement.statements[0])
            assert alternative_statement.expression is not None
            self._test_identifier(alternative_statement.expression, 'z')

    def test_if_else_if_expression(self) -> None:
            source: str = '''
            si (x == 5) { 
                regresa verdadero; 
            } si_no si (x > 5){
                regresa x;
            } si_no {
                z;
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
            
            consecuence_statement = cast(ReturnStatement, if_expresion.consecuence.statements[0])
            assert consecuence_statement.return_value is not None
            self._test_literal_expression(consecuence_statement.return_value, True)

            #Test alternative
            assert if_expresion.alternative is not None
            self.assertIsInstance(if_expresion.alternative, If)
            else_if = cast(If, if_expresion.alternative)

            #Test condition
            assert else_if.condition is not None
            self._test_infix_expression(else_if.condition, 'x','>', 5)

            #Test consecuence
            assert else_if.consecuence is not None
            self.assertIsInstance(else_if.consecuence, Block)
            self.assertEquals(len(else_if.consecuence.statements),1)

            consecuence_statement = cast(ReturnStatement, else_if.consecuence.statements[0])
            assert consecuence_statement.return_value is not None
            self._test_identifier(consecuence_statement.return_value,  'x')

            #Test alternative
            assert else_if.alternative is not None
            self.assertIsInstance(else_if.alternative, Block)
            alternative_statement = cast(Block, else_if.alternative)
            self.assertEquals(len(alternative_statement.statements),1)
            indetifier_statement = cast(ExpressionStatement, alternative_statement.statements[0])
            assert indetifier_statement.expression is not None
            self._test_identifier(indetifier_statement.expression, 'z')


    def test_function_literal(self) -> None:
        source: str = 'metodo suma(x,y) { x + y}'
        lexer: Lexer = Lexer(source) 
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        # Test correct node type
        function_literal = cast(Function, cast(ExpressionStatement, program.statements[0]).expression)
        self.assertIsInstance(function_literal, Function)
        #Test correct name
        self.assertIsInstance(function_literal.name, Identifier)
        function_name = cast(Identifier, function_literal.name)
        self.assertEquals(function_name.value, "suma")
        self.assertEquals(function_name.token.literal, "suma")
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

    def test_lambda_literal(self) -> None:
        source: str = 'procedimiento(x,y) { x + y}'
        lexer: Lexer = Lexer(source) 
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        # Test correct node type
        function_literal = cast(Lambda, cast(ExpressionStatement, program.statements[0]).expression)

        self.assertIsInstance(function_literal, Lambda)

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

            function = cast(Lambda, cast(ExpressionStatement,program.statements[0]).expression)
            self.assertEquals(len(function.parameters), len(test['expected_params']))

            for idx, param in enumerate(test['expected_params']):
                self._test_literal_expression(function.parameters[idx], param)

    def test_call_expression(self) -> None:
        source: str = 'suma(1, 2 * 3, 4 + 5,8.21);'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        call = cast(Call, cast(ExpressionStatement,program.statements[0]).expression)

        self.assertIsInstance(call, Call)
        self._test_identifier(call.function, 'suma')

        #Test arguments
        assert call.arguments is not None
        self.assertEquals(len(call.arguments), 4)
        self._test_literal_expression(call.arguments[0], 1)
        self._test_infix_expression(call.arguments[1], 2, '*', 3)
        self._test_infix_expression(call.arguments[2], 4, '+', 5)
        self._test_literal_expression(call.arguments[3], 8.21)

    def test_string_literal_expression(self) -> None:
        source: str = '"hello world!"'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        expression_statement = cast(ExpressionStatement, program.statements[0])
        string_literal = cast(StringLiteral, expression_statement.expression)

        self.assertIsInstance(string_literal, StringLiteral)
        self.assertEquals(string_literal.value, 'hello world!')

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
        elif value_type == float:
            self._test_float(expression, expected_value)
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

    def _test_float(self,
                        expression: Expression,
                        expected_value:float)-> None:
        self.assertIsInstance(expression,Float)

        floating = cast(Float, expression)
        self.assertEquals(floating.value, expected_value)
        self.assertEquals(floating.token.literal, str(expected_value))

        