from unittest import TestCase
from typing import (List,cast,Any,Type,Tuple,Union)

from kp.ast import Program
from kp.evaluator import (evaluate, NULL)
from kp.lexer import Lexer
from kp.parser import Parser
from kp.object import(
    Error,
    Float,
    Object,
    String,
    Integer,
    Boolean,
    Function,
    Environment,
)

class EvaluatorTest(TestCase):

    def test_integer_evaluator(self)-> None:
        test: List[Tuple[str, int]] = [
            ('5',5),
            ('10',10),
            ('-5',-5),
            ('-10',-10),
            ('5+5',10),
            ('5-10',-5),
            ('2*2*2*2',16),
            ('2*5-3',7),
            ('parsearAentero(50 / 2)',25),
            ('2 * (5 - 3)',4),
            ('parsearAentero((2 + 7) / 3)',3),
            ('parsearAentero(50 / 2 * 2 + 10)',60),
        ]
        for source, expected in test:
            evaluated = self._evaluate_test(source)
            self._test_integer_object(evaluated, expected)

    def test_float_evaluator(self)-> None:
        test: List[Tuple[str, float]] = [
            ('1.3324',1.3324),
            ('10.978',10.978),
            ('-5.134',-5.134),
            ('-10.112',-10.112),
            ('5+5.34',10.34),
            ('5-10.1',-5.1),
            ('2.6*3.9*4.1',41.574),
            ('5 / 2',2.5),
        ]
        for source, expected in test:
            print(source)
            evaluated = self._evaluate_test(source)
            self._test_float_object(evaluated, expected)

    def test_raise_to_n_power(self)-> None:
        test: List[Tuple[str, Any]] = [
            ('2 **2',4),
            ('2 ** 20',1048576),
            ('-7 ** 5',-16807),
            ('4.38 ** 2',19.1844),
            ('3.7 ** 9.5',249986.39782813037),
            ('7 ** -2',0.02040816326530612),
            ('20 + 2 ** 4 / 2',28.0),
            ('5**2 + 20 *5 + 30',155),
        ]
        for source, expected in test:
            print(source)
            evaluated = self._evaluate_test(source)
            if type(expected) == float:
                self._test_float_object(evaluated, expected)
            elif type(expected) == int:
               self._test_integer_object(evaluated, expected) 

    def test_module_evaluator(self)-> None:
        test: List[Tuple[str, Any]] = [
            ('5 %5',0),
            ('55.66 % 15.55',9.009999999999994),
            ('32 % 3',2),
            ('0.111 % 0.2',0.111),
            ('90 % 9',0),
            ('24.75 % 32',24.75),
        ]
        for source, expected in test:
            print(source)
            evaluated = self._evaluate_test(source)
            if type(expected) == float:
                self._test_float_object(evaluated, expected)
            elif type(expected) == int:
               self._test_integer_object(evaluated, expected) 

    def test_boolean_evaluation(self)-> None:
        test: List[Tuple[str,bool]] = [
            ('verdadero', True),
            ('falso', False),
            ('1 < 2', True),
            ('1 > 2', False),
            ('1 < 1', False),
            ('1 > 1', False),
            ('1 == 1', True),
            ('1 != 1', False),
            ('1 != 2', True),

            ('1.99 < 2', True),
            ('1.8 > 1.85', False),
            ('1.99 < 1.98', False),
            ('1.777 > 1.78', False),
            ('1.565 == 1.56500', True),
            ('21.3 != 21.3', False),
            ('111.656 != 111.654', True),

            ('verdadero == verdadero', True),
            ('falso == falso', True),
            ('verdadero == falso', False),
            ('verdadero != falso', True),

            ('(1 < 2) == verdadero', True),
            ('(1 < 2) == falso', False),
            ('(1 > 2) == verdadero', False),
            ('(1 > 2) == falso', True),
        ]

        for source, expected in test:
            print(source)
            evaluated = self._evaluate_test(source)
            self._test_boolean_object(evaluated,expected)

    def test_bang_operator(self) -> None:
        test: List[Tuple[str, bool]] = [
          ('!verdadero', False),  
          ('!falso', True), 
          ('!!falso', False),
          ('!!verdadero', True),
          ('!5', False),
          ('!!5', True),
        ]
        for source, expected in test:
            evaluated = self._evaluate_test(source)
            self._test_boolean_object(evaluated, expected)
    
    def test_if_else_evaluation(self) -> None:
        test: List[Tuple[str, Any]] = [
            ('si (verdadero) { 10; }', 10),
            ('si (falso) { 10; }', None),
            ('si (1) { 10; }', None),
            ('si (1 < 2) { 10; }', 10),
            ('si (1 > 2) { 10; }', None),
            ('si (1 < 2) { 10; } si_no {20;}', 10),
            ('si (1 > 2) { 10; } si_no {20;}', 20),
        ]
        for source, expected in test:
            evaluated = self._evaluate_test(source)
            if type(expected) == int:
                self._test_integer_object(evaluated, expected)
            else:
                self._test_null_object(evaluated)

    def  test_return_evaluation(self) -> None:
        test: List[Tuple[str, int]] = [
            ('regresa 10;' , 10),
            ('regresa 10; 9;' , 10),
            ('regresa 2*5; 9;' , 10),
            (' 9; regresa 3*6; 9;' , 18),
            ('''
                si(10 > 1){
                   si (20 > 10){
                    regresa 1;
                   } 
                   regresa 0;
                }
            ''' , 1),
            ('''
                si(10 >= 1){
                   si (20 >= 20){
                    regresa 1;
                   } 
                   regresa 0;
                }
            ''' , 1),
            ('''
                si(10 <= 10){
                   si (20 <= 19){
                    regresa 1;
                   } 
                   regresa 0;
                }
            ''' , 0),
        ]
        for source, expected in test:
            evaluated = self._evaluate_test(source)
            self._test_integer_object(evaluated, expected)

    def test_error_handling(self) -> None:
        test: List[Tuple[str, str]] = [
            ('5 + verdadero',
            'Poseemos un problema, no puedo ejecutar INTEGER + BOOLEAN'),
            ('5 + verdadero; 9;',
            'Poseemos un problema, no puedo ejecutar INTEGER + BOOLEAN'),
            ('-verdadero;',
            'Poseemos un problema, no puedo operar -BOOLEAN'),
            ('verdadero-verdadero;',
            'Poseemos un problema, no puedo operar BOOLEAN - BOOLEAN'),
            ('5; verdadero+falso; 10;',
            'Poseemos un problema, no puedo operar BOOLEAN + BOOLEAN'),
            ('''
                si (10 > 7){
                    regresa verdadero + falso;
                }
            ''',
            'Poseemos un problema, no puedo operar BOOLEAN + BOOLEAN'),
            ('''
                si (10 > 1){
                    si(verdadero){
                        regresa verdadero * falso;
                    }
                    regresa 1;
                }
            ''',
            'Poseemos un problema, no puedo operar BOOLEAN * BOOLEAN'),
            ('''
                si (5 < 2){
                    regresa 1;
                } si_no {
                    regresa verdadero / falso;
                }
            ''',
            'Poseemos un problema, no puedo operar BOOLEAN / BOOLEAN'),
            ('''
                foobar;
            ''',
            'Poseemos un problema, que es "foobar"?'),
            ( '"foo" - "bar";',
            'Poseemos un problema, no puedo operar STRING - STRING'),
            ( 'pies = 31;',
            'Poseemos un problema, que es "pies"?'),
            ( 'variable manos = "marco"; pies = "hola"; manos+pies;',
            'Poseemos un problema, que es "pies"?'),
        ]

        for source, expected in test:
            print(source)
            evaluated = self._evaluate_test(source)

            self. assertIsInstance(evaluated, Error)

            evaluated = cast(Error, evaluated)
            self.assertEquals(evaluated.message, expected)

    def test_assignment_evaluation(self) -> None:
        test: List[Tuple[str, int]] = [
            ('variable a = 5; a;', 5),
            ('variable a = 5 * 5; a;', 25),
            ('variable a = 5; variable b = a; b;', 5),
            ('variable a = 5; variable b = a; variable c = a + b + 5; c;', 15),
            ('variable a = 5; a=10; a;',10),
            ('variable a = 15; a=100; variable b = 200; variable c = a+b; c;',300),
        ]

        for source, expected in test:
            evaluated = self._evaluate_test(source)
            self._test_integer_object(evaluated, expected)

    def test_function_evaluation(self) -> None:
        source: str = 'procedimiento(x) {x + 2;};'

        evaluated = self._evaluate_test(source)
        self.assertIsInstance(evaluated,Function)

        evaluated = cast(Function, evaluated)
        self.assertEquals(len(evaluated.parameters),1)
        self.assertEquals(str(evaluated.parameters[0]), 'x')
        self.assertEquals(str(evaluated.body), '(x + 2)')

    def test_function_calls(self) -> None:
        test: List[Tuple[str, int]] = [
            ('variable identidad = procedimiento(x) {x;}; identidad(5);', 5),
            ('''
            variable identidad = procedimiento(x){
                regresa x;
            };
            identidad(5);
            ''',5),
            ('''
            variable doble = procedimiento(x){
                regresa 2* x;
            };
            doble(5);
            ''',10),
            ('''
            variable suma = procedimiento(x, y){
                regresa x + y;
            };
            suma(3,8);
            ''',11),
            ('''
            variable suma = procedimiento(x, y){
                regresa x + y;
            };
            suma(5 + 5, suma(10,10));
            ''',30),
            ('procedimiento(x){x;} (5)', 5),
        ]
        for source, expected in test:
            evaluated = self._evaluate_test(source)
            self._test_integer_object(evaluated,expected)
    
    def test_string_evaluation(self) -> None:
        test: List[Tuple[str, str]] = [
            ('"Hello world!"', 'Hello world!'),
            ('procedimiento() { regresa "Kinp es re-genial"; } ()',
            'Kinp es re-genial')
        ]
        for source, expected in test:
            evaluated = self._evaluate_test(source)
            self.assertIsInstance(evaluated,String)

            evaluated = cast(String, evaluated)
            self.assertEquals(evaluated.value, expected)

    def test_string_concatenation(self) -> None:
        test: List[Tuple[str,str]] = [
            ('"FOO" + "BAR";', 'FOOBAR'),
            ('"Hello," + " " +"world!";', 'Hello, world!'),
            ('''
                variable saludo = procedimiento(nombre) {
                    regresa "Hola " + nombre + "!";
                };
                saludo("Marco");
            ''', 
            'Hola Marco!'),
        ]

        for source, expected in test:
            evaluated = self._evaluate_test(source)
            self._test_string_object(evaluated, expected)

    def test_string_comparation(self) -> None:
        test: List[Tuple[str, bool]] = [
            ('"a" == "a"', True),
            ('"a" != "a"', False),
            ('"a" == "A"', False),
            ('"a" != "A"', True),
        ]

        for source, expected in test:
            evaluated = self._evaluate_test(source)
            self._test_boolean_object(evaluated, expected)

    def test_builtin_functions(self) -> None:
            #('imprimir("uno", "dos");', 'Poseemos un problema, numero incorrecto de argumentos, se requeria 1, pero se recibio 2'),
            #('imprimir(1);', "1"),
            #('imprimir(2*3*4);', "24"),
            #('imprimir((((2+3)*(4*7))/5));', "28"),
            #('variable edad = procedimiento() {regresa verdadero; };imprimir(edad());', "verdadero"),
        test: List[Tuple[str,Union[str,int,bool]]] = [
            ('longitud("");', 0),
            ('longitud("cuatro");', 6),
            ('longitud("Hola mundo");', 10),

            ('parsearAentero("1564");', 1564),
            ('parsearAentero("-1564");', -1564),
            ('parsearAentero(verdadero);', 1),
            ('parsearAentero(falso);', 0),

            ('parsearAtexto(99999);', "99999"),
            ('parsearAtexto(verdadero);', "verdadero"),
            ('parsearAtexto(falso);', "falso"),

            ('parsearAbooleano(1);', True),
            ('parsearAbooleano(0);', False),
            ('parsearAbooleano(24);', False),
        ]
        for source, expected in test:
            evaluated = self._evaluate_test(source)
            print(source)
            if type(expected) == int:
                expected = cast(int, expected)
                self._test_integer_object(evaluated, expected)
            elif type(expected) == bool:
                expected = cast(bool, expected)
                self._test_boolean_object(evaluated,expected)
            else:
                expected = cast(str, expected)
                self._test_string_object(evaluated, expected)

    def test_builtin_functions_errors(self) -> None:
        test: List[Tuple[str,str]] = [
            ('longitud(1);', 'Poseemos un problema, no tengo soporte para INTEGER'),
            ('longitud("uno", "dos");', 'Poseemos un problema, numero incorrecto de argumentos, se requeria 1, pero se recibio 2'),
            ('parsearAentero("veinte");', 'Poseemos un problema, "veinte" no es numero y no se puede castear'),
            ('parsearAbooleano("verdadero");', 'Poseemos un problema, no tengo soporte para STRING'),
        ]
        for source, expected in test:
            evaluated = self._evaluate_test(source)
            expected = cast(str, expected)
            self._test_error_object(evaluated, expected)

###############################################AUXILIAR FUNCTIONS###############################################

    def _evaluate_test(self, source: str) -> Object:
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()
        env: Environment = Environment()
        
        evaluated = evaluate(program,env)
        assert evaluated is not None
        return evaluated

    def _test_null_object(self, evaluated: object) -> None:
        self.assertEquals(evaluated, NULL)

    def _test_boolean_object(self, evaluated: Object, expected: bool) -> None:
        self.assertIsInstance(evaluated, Boolean)
        
        evaluated = cast(Boolean, evaluated)
        self.assertEquals(evaluated.value, expected)
    
    def _test_integer_object(self, evaluated: Object, expected: int) -> None:
        self.assertIsInstance(evaluated, Integer)

        evaluated = cast(Integer, evaluated)
        self.assertEquals(evaluated.value, expected)

    def _test_float_object(self, evaluated: Object, expected: float) -> None:
        self.assertIsInstance(evaluated, Float)

        evaluated = cast(Float, evaluated)
        self.assertEquals(evaluated.value, expected)

    def _test_string_object(self, evaluated:Object, expected:str) -> None:
        self.assertIsInstance(evaluated, String)

        evaluated = cast(String, evaluated)
        self.assertEquals(evaluated.value,expected)

    def _test_error_object(self, evaluated: Object, expected: str) -> None:
        self.assertIsInstance(evaluated, Error)

        evaluated = cast(Error, evaluated)
        self.assertEquals(evaluated.message, expected)
