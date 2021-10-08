import unittest

import pytest

import monkey.ast as AST
import monkey.objects as OBJ
from monkey.environment import Environment
from monkey.evaluator import Evaluator
from monkey.objects import Function
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
            ("true == true", True),
            ("false == false", True),
            ("true == false", False),
            ("true != false", True),
            ("false != true", True),
            ("(1 < 2) == true", True),
            ("(1 < 2) == false", False),
            ("(1 > 2) == true", False),
            ("(1 > 2) == false", True),
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

    def test_if_else_expressions(self):
        tests = [
            ("if (true) { 10 }", 10),
            ("if (false) { 10 }", None),
            ("if (1) { 10 }", 10),
            ("if (1 < 2) { 10 }", 10),
            ("if (1 > 2) { 10 }", None),
            ("if (1 > 2) { 10 } else { 20 }", 20),
            ("if (1 < 2) { 10 } else { 20 }", 10),
        ]

        for t in tests:
            evaluated = self.test_eval(t[0])
            if isinstance(t[1], int):
                self.test_integer_object(evaluated, t[1])
            else:
                self.test_null_object(evaluated)

    def test_return_statements(self):
        tests = [

            (r'''
                if (10 > 1) {
                    if (10 > 1) {
                        return 10;
                    }

                    return 1;
                }''', 10),
        ]

        for t in tests:
            evaluated = self.test_eval(t[0])
            assert self.test_integer_object(evaluated, t[1])

    def test_error_handling(self):
        tests = [
            (
                "5 + true;",
                "Type mismatch: INTEGER + BOOLEAN",
            ),
            (
                "5 + true; 5;",
                "Type mismatch: INTEGER + BOOLEAN",
            ),
            (
                "-true",
                "Unknown operator: -BOOLEAN",
            ),
            (
                "true + false;",
                "Unknown operator: BOOLEAN + BOOLEAN",
            ),
            (
                "5; true + false; 5",
                "Unknown operator: BOOLEAN + BOOLEAN",
            ),
            (
                "if (10 > 1) { true + false; }",
                "Unknown operator: BOOLEAN + BOOLEAN",
            ),
            (
                r'''
    if (10 > 1) {
    if (10 > 1) {
        return true + false;
    }

    return 1;
    }''', "Unknown operator: BOOLEAN + BOOLEAN",
            ),
            ("foobar", "Identifier not found: foobar"),
        ]

        for t in tests:
            print(t[0])
            evaluated = self.test_eval(t[0])
            assert evaluated.message == t[1]

    def test_let_statements(self):
        tests = [
            ("let a = 5; a;", 5),
            ("let a= 5 * 5; a;", 25),
            ("let a = 5; let b = a; b;", 5),
            ("let a= 5; let b= a; let c = a + b + 5; c;", 15),
        ]

        for test in tests:
            self.test_integer_object(self.test_eval(test[0]), test[1])

    def test_function_object(self):
        input = "fn(x) { x + 2; };"

        fn: Function = self.test_eval(input)
        
        assert len(fn.parameters) == 1
        assert str(fn.parameters[0]) == "x"
        assert str(fn.body) == "(x + 2)"

    def test_function_application(self):
        tests = [
            ("let identity = fn(x) { x; }; identity(5);", 5),
            ("let identity = fn(x) { return x; }; identity(5);", 5),
            ("let double = fn(x) { x * 2; }; double(5);", 10),
            ("let add = fn(x, y) { x + y; }; add(5, 5);", 10),
            ("let add = fn(x, y) { x + y; }; add(5 + 5, add(5, 5));", 20),
            ("fn(x) { x; }(5)", 5),
        ]

        for t in tests:
            self.test_integer_object(self.test_eval(t[0]), t[1])

    @pytest.mark.skip(reason="Don't test helper function")
    def test_eval(self, input: str) -> Object:
        l = Lexer(input)
        p = Parser(l)
        program = p.parse_program()
        env = Environment()
        return Evaluator().eval(program, env)

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

    @pytest.mark.skip(reason="Don't test helper function")
    def test_null_object(self, obj: Object) -> bool:
        if not obj:
            return True
        return False
