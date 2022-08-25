from unittest import TestCase
from typing import (List,cast,Any,Type,Tuple)

from kp.ast import Program
from kp.evaluator import evaluate
from kp.lexer import Lexer
from kp.parser import Parser
from kp.object import(
    Object,
    Integer,
    Boolean,
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
            ('50 / 2',25),
            ('2 * (5 - 3)',4),
            ('(2 + 7) / 3',3),
            ('50 / 2 * 2 + 10',60),
            ('5 / 2',2),
        ]
        for source, expected in test:
            evaluated = self._evaluate_test(source)
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

###############################################AUXILIAR FUNCTIONS###############################################
    
    def _evaluate_test(self, source: str) -> Object:
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        evaluated = evaluate(program)
        assert evaluated is not None
        return evaluated

    def _test_boolean_object(self, evaluated: Object, expected: bool) -> None:
        self.assertIsInstance(evaluated, Boolean)
        
        evaluated = cast(Boolean, evaluated)
        self.assertEquals(evaluated.value, expected)
    
    def _test_integer_object(self, evaluated: Object, expected: int) -> None:
        self.assertIsInstance(evaluated, Integer)

        evaluated = cast(Integer, evaluated)
        self.assertEquals(evaluated.value, expected)
