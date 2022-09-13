from unittest import TestCase
from typing import List

from kp.token import(
    Token,
    TokenType,
)
from kp.lexer import Lexer

class LexerTest(TestCase):

    def _get_tokens(self, source : str, lenght:int) -> List[Token]:
        lexer: Lexer = Lexer(source)
        tokens: List[Token] = []

        for i in range(lenght):
            tokens.append(lexer.next_token())
        
        return tokens
        
    def test_illegal(self) -> None:
        source: str = '¡¿@'
        expected_tokens: List[Token] = [
            Token(TokenType.ILLEGAL, '¡'),
            Token(TokenType.ILLEGAL, '¿'),
            Token(TokenType.ILLEGAL, '@'),
        ]
        self.assertEquals(self._get_tokens(source,len(source)), expected_tokens)
    
    def test_one_character_operator(self) -> None:
        source: str = '=+-/*<>!'
        expected_tokens: List[Token] = [
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.PLUS, '+'),
            Token(TokenType.LESS, '-'),
            Token(TokenType.DIVISION, '/'),
            Token(TokenType.MULTIPLICATION, '*'),
            Token(TokenType.LT, '<'),
            Token(TokenType.GT, '>'),
            Token(TokenType.NEGATION, '!'),
        ]
        self.assertEquals(self._get_tokens(source,len(source)), expected_tokens)

    def test_eof(self) -> None:
        source: str = '+'
        expected_tokens: List[Token] = [
            Token(TokenType.PLUS, '+'),
            Token(TokenType.EOF, '')
        ]
        self.assertEquals(self._get_tokens(source,len(source)+1), expected_tokens)

    def test_delimiters(self) -> None:
        source: str = '(){},;'
        expected_tokens: List[Token] = [
              Token(TokenType.LPAREN, '('),
              Token(TokenType.RPAREN, ')'),
              Token(TokenType.LBRACE, '{'),
              Token(TokenType.RBRACE, '}'),
              Token(TokenType.COMMA, ','), 
              Token(TokenType.SEMICOLON, ';'),   
        ]        
        self.assertEquals(self._get_tokens(source,len(source)), expected_tokens)
    
    def test_assignment(self) -> None:
        source: str = '''variable cinco = 5;
        variable cinco = 5.0;'''
        expected_tokens: List[Token] = [
            Token(TokenType.LET, 'variable'),
            Token(TokenType.IDENT, 'cinco'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.INT, '5'),
            Token(TokenType.SEMICOLON, ';'),

            Token(TokenType.LET, 'variable'),
            Token(TokenType.IDENT, 'cinco'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.FLOAT, '5.0'),
            Token(TokenType.SEMICOLON, ';'),
        ]
        self.assertEquals(self._get_tokens(source,10), expected_tokens)
    
    def test_lamda_declaration(self) -> None:
        source: str = '''variable suma = procedimiento(x,y){
            x+y;
        };'''
        expected_tokens: List[Token] = [
            Token(TokenType.LET, 'variable'),
            Token(TokenType.IDENT, 'suma'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.LAMBDA, 'procedimiento'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.IDENT, 'x'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.IDENT, 'y'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.IDENT, 'x'),
            Token(TokenType.PLUS, '+'),
            Token(TokenType.IDENT, 'y'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.RBRACE, '}'),
            Token(TokenType.SEMICOLON, ';'),
        ] 
        self.assertEquals(self._get_tokens(source,16), expected_tokens)

    def test_function_declaration(self) -> None:
        source: str = '''metodo suma(x,y){
            x+y;
        }'''
        expected_tokens: List[Token] = [
            Token(TokenType.FUNCTION, 'metodo'),
            Token(TokenType.IDENT, 'suma'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.IDENT, 'x'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.IDENT, 'y'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.IDENT, 'x'),
            Token(TokenType.PLUS, '+'),
            Token(TokenType.IDENT, 'y'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.RBRACE, '}'),
        ] 
        self.assertEquals(self._get_tokens(source,13), expected_tokens)

    def test_function_call(self) -> None:
        source : str = 'variable resultado = suma(dos,tres);'
        expected_tokens: List[Token] = [
            Token(TokenType.LET, 'variable'),
            Token(TokenType.IDENT, 'resultado'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.IDENT, 'suma'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.IDENT, 'dos'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.IDENT, 'tres'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.SEMICOLON, ';'),
        ]
        self.assertEquals(self._get_tokens(source,10), expected_tokens)

    def test_control_statement(self) -> None:
        source : str = '''
        si (5 < 10) {
            regresa verdadero;
        } si_no {
            regresa falso;
        }
        '''
        expected_tokens: List[Token] = [
            Token(TokenType.IF, 'si'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.INT, '5'),
            Token(TokenType.LT, '<'),
            Token(TokenType.INT, '10'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.RETURN, 'regresa'),
            Token(TokenType.TRUE, 'verdadero'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.RBRACE, '}'),
            Token(TokenType.ELSE, 'si_no'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.RETURN, 'regresa'),
            Token(TokenType.FALSE, 'falso'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.RBRACE, '}'),
        ]
        self.assertEquals(self._get_tokens(source,17), expected_tokens)
    
    def test_two_character_operator(self) -> None:
        source: str = '''
            10 == 11;
            10 != 19;
            11 >= 12;
            222 <= 212;
            33 >= 33;
            -90 >= -90;
        '''
        expected_tokens: List[Token] = [
            Token(TokenType.INT, '10'),
            Token(TokenType.EQ, '=='),
            Token(TokenType.INT, '11'),
            Token(TokenType.SEMICOLON, ';'),

            Token(TokenType.INT, '10'),
            Token(TokenType.NOT_EQ, '!='),
            Token(TokenType.INT, '19'),
            Token(TokenType.SEMICOLON, ';'),

            Token(TokenType.INT, '11'),
            Token(TokenType.GEQT, '>='),
            Token(TokenType.INT, '12'),
            Token(TokenType.SEMICOLON, ';'),

            Token(TokenType.INT, '222'),
            Token(TokenType.LEQT, '<='),
            Token(TokenType.INT, '212'),
            Token(TokenType.SEMICOLON, ';'),

            Token(TokenType.INT, '33'),
            Token(TokenType.GEQT, '>='),
            Token(TokenType.INT, '33'),
            Token(TokenType.SEMICOLON, ';'),

            Token(TokenType.LESS, '-'),
            Token(TokenType.INT, '90'),
            Token(TokenType.GEQT, '>='),
            Token(TokenType.LESS, '-'),
            Token(TokenType.INT, '90'),
            Token(TokenType.SEMICOLON, ';'),
        ]
        self.assertEquals(self._get_tokens(source,26), expected_tokens)

    def test_two_character_operator_float(self) -> None:
        source: str = '''
            10.6 == 11.9;
            10.7 != 19;
            11.54 >= 12;
            222.2 <= 212.001;
            33.5432 >= 33.1;
            -90.95344 >= -90.9999;
        '''
        expected_tokens: List[Token] = [
            Token(TokenType.FLOAT, '10.6'),
            Token(TokenType.EQ, '=='),
            Token(TokenType.FLOAT, '11.9'),
            Token(TokenType.SEMICOLON, ';'),

            Token(TokenType.FLOAT, '10.7'),
            Token(TokenType.NOT_EQ, '!='),
            Token(TokenType.INT, '19'),
            Token(TokenType.SEMICOLON, ';'),

            Token(TokenType.FLOAT, '11.54'),
            Token(TokenType.GEQT, '>='),
            Token(TokenType.INT, '12'),
            Token(TokenType.SEMICOLON, ';'),

            Token(TokenType.FLOAT, '222.2'),
            Token(TokenType.LEQT, '<='),
            Token(TokenType.FLOAT, '212.001'),
            Token(TokenType.SEMICOLON, ';'),

            Token(TokenType.FLOAT, '33.5432'),
            Token(TokenType.GEQT, '>='),
            Token(TokenType.FLOAT, '33.1'),
            Token(TokenType.SEMICOLON, ';'),

            Token(TokenType.LESS, '-'),
            Token(TokenType.FLOAT, '90.95344'),
            Token(TokenType.GEQT, '>='),
            Token(TokenType.LESS, '-'),
            Token(TokenType.FLOAT, '90.9999'),
            Token(TokenType.SEMICOLON, ';'),
        ]
        self.assertEquals(self._get_tokens(source,26), expected_tokens)

    def test_string(self) -> None:
        source: str = '''
        "foo";
        "Kinp es el mejor lenguaje de Programacion";
        '''
        expected_tokens: List[Token] =[
            Token(TokenType.STRING, 'foo'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.STRING, 'Kinp es el mejor lenguaje de Programacion'),
            Token(TokenType.SEMICOLON, ';'),
        ]
        self.assertEquals(self._get_tokens(source,4),expected_tokens)

    def test_raised_to_n_power(self) -> None:
        source: str = '''
            2 ** 4;
            -23 ** 9;
            -10 ** -10;
            -4.5 ** 2.5;
        '''
        expected_tokens: List[Token] = [
            Token(TokenType.INT, '2'),
            Token(TokenType.RTP, '**'),
            Token(TokenType.INT, '4'),
            Token(TokenType.SEMICOLON, ';'),

            Token(TokenType.LESS, '-'),
            Token(TokenType.INT, '23'),
            Token(TokenType.RTP, '**'),
            Token(TokenType.INT, '9'),
            Token(TokenType.SEMICOLON, ';'),

            Token(TokenType.LESS, '-'),
            Token(TokenType.INT, '10'),
            Token(TokenType.RTP, '**'),
            Token(TokenType.LESS, '-'),
            Token(TokenType.INT, '10'),
            Token(TokenType.SEMICOLON, ';'),

            Token(TokenType.LESS, '-'),
            Token(TokenType.FLOAT, '4.5'),
            Token(TokenType.RTP, '**'),
            Token(TokenType.FLOAT, '2.5'),
            Token(TokenType.SEMICOLON, ';'),
        ]
        self.assertEquals(self._get_tokens(source,20), expected_tokens)

    def test_module_operation(self) -> None:
        source: str = '''
        5 % 5;
        30 % 2;
        25 % 9;
        -90 % 9;
        24.75 % -32;
        '''
        expected_tokens: List[Token] = [
            Token(TokenType.INT, '5'),
            Token(TokenType.MOD, '%'),
            Token(TokenType.INT, '5'),
            Token(TokenType.SEMICOLON, ';'),

            Token(TokenType.INT, '30'),
            Token(TokenType.MOD, '%'),
            Token(TokenType.INT, '2'),
            Token(TokenType.SEMICOLON, ';'),

            Token(TokenType.INT, '25'),
            Token(TokenType.MOD, '%'),
            Token(TokenType.INT, '9'),
            Token(TokenType.SEMICOLON, ';'),

            Token(TokenType.LESS, '-'),
            Token(TokenType.INT, '90'),
            Token(TokenType.MOD, '%'),
            Token(TokenType.INT, '9'),
            Token(TokenType.SEMICOLON, ';'),

            Token(TokenType.FLOAT, '24.75'),
            Token(TokenType.MOD, '%'),
            Token(TokenType.LESS, '-'),
            Token(TokenType.INT, '32'),
            Token(TokenType.SEMICOLON, ';'),
        ]
        self.assertEquals(self._get_tokens(source,22), expected_tokens)
