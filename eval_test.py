import unittest

import pytest

import monkey.ast as AST
import monkey.objects as OBJ
from monkey.evaluator import Evaluator
from monkey.lexer import Lexer
from monkey.parser import Parser
from monkey.objects import Object


class EvalTest(unittest.TestCase):
    def test_eval_integer_expression(self):
        tests = [
            ("5", 5),
            ("10", 10),
            ("-5", -5),
            ("-10", -10),
            ("5 + 5 + 5 + 5 - 10", 10),
            ("2 * 2 * 2 * 2 * 2", 32),
            ("-50 + 100 + -50", 0),
            ("5 * 2 + 10", 20),
            ("5 + 2 * 10", 25),
            ("20 + 2 * -10", 0),
            ("50 / 2 * 2 + 10", 60),
            ("2 * (5 + 10)", 30),
            ("3 * 3 * 3 + 10", 37),
            ("3 * (3 * 3) + 10", 37),
            ("(5 + 10 * 2 + 15 / 3) * 2 + -10", 50),
        ]

        for t in tests:
            evaluated = self.test_eval(t[0])
            self.test_integer_object(evaluated, t[1])

    def test_eval_boolean_expression(self):
        tests = [
            ("true", True),
            ("false", False),
            ("1 < 2", True),
            ("1 > 2", False),
            ("1 < 1", False),
            ("1 > 1", False),
            ("1 == 1", True),
            ("1 != 1", False),
            ("1 == 2", False),
            ("1 != 2", True),
        ]

        for t in tests:
            evaluated = self.test_eval(t[0])
            self.test_boolean_object(evaluated, t[1])

    def test_eval_bang_operators(self):
        tests = [
            ("!true", False),
            ("!false", True),
            ("!5", False),
            ("!!true", True),
            ("!!false", False),
            ("!!5", True),
        ]

        for t in tests:
            evaluated = self.test_eval(t[0])
            self.test_boolean_object(evaluated, t[1])

    @pytest.mark.skip(reason="Don't test helper function")
    def test_eval(self, input: str) -> Object:
        l = Lexer(input)
        p = Parser(l)
        program = p.parse_program()
        return Evaluator().eval(program)

    @pytest.mark.skip(reason="Don't test helper function")
    def test_integer_object(self, obj: Object, expected: int) -> bool:
        result: OBJ = obj
        if result.value != expected:
            return False
        return True

    @pytest.mark.skip(reason="Don't test helper function")
    def test_boolean_object(self, obj: Object, expected: bool) -> bool:
        result: OBJ = obj
        if result.value != expected:
            return False
        return True
