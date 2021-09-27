import unittest

import pytest

import monkey.ast as AST
from monkey.lexer import Lexer
from monkey.parser import Parser
from monkey.token import Token, TokenType


class ParserTest(unittest.TestCase):
    def test_let_statements(self):
        input = r'''
    let x = 5;
    let y = 10;
    let foobar = 838383;
    '''

        l = Lexer(input)
        p = Parser(l)

        program = p.parse_program()
        assert program is not None
        assert len(program.statements) == 3

        tests = ["x", "y", "foobar"]
        for i, tt in enumerate(tests):
            statement = program.statements[i]
            assert self.match_let_statement(statement, tt)

    def match_let_statement(self, stmt: AST.Statement, name: str) -> bool:
        assert stmt.token_literal() == "let"

        let_stmt: AST.LetStatement = stmt
        assert let_stmt.name.value == name
        assert let_stmt.name.token_literal() == name
        return True

    def test_return_statements(self):
        input = r'''
    return 5;
    return 10;
    return 838383;
    '''

        l = Lexer(input)
        p = Parser(l)

        program = p.parse_program()
        assert program is not None
        assert len(program.statements) == 3

        tests = ["x", "y", "foobar"]
        for i, tt in enumerate(tests):
            statement = program.statements[i]
            assert statement.token_literal() == "return"

    def test_identifier_expression(self):
        input = "foobar"

        l = Lexer(input)
        p = Parser(l)
        program = p.parse_program()
        assert len(program.statements) == 1

        stmt: AST.ExpressionStatement = program.statements[0]
        ident: AST.Identifier = stmt.expression
        assert ident.value == "foobar"
        assert ident.token_literal() == "foobar"

    def test_integer_literal_expression(self):
        input = "5"

        l = Lexer(input)
        p = Parser(l)
        program = p.parse_program()
        assert len(program.statements) == 1

        stmt: AST.ExpressionStatement = program.statements[0]
        literal: AST.IntegerLiteral = stmt.expression
        assert literal.value == 5
        assert literal.token_literal() == "5"

    def test_parsing_prefix_expressions(self):
        prefix_tests = [
            ("!5;", "!", 5),
            ("-15;", "-", 15),
            ("!true;", "!", True),
            ("!false;", "!", False),
        ]

        for test in prefix_tests:
            l = Lexer(test[0])
            p = Parser(l)
            program = p.parse_program()
            assert len(program.statements) == 1

            stmt: AST.ExpressionStatement = program.statements[0]
            exp: AST.PrefixExpression = stmt.expression
            assert exp.operator == test[1]
            assert exp.right.value == test[2]

    def test_parsing_infix_expression(self):
        infix_tests = [
            # input, left_value, operator, right_value
            ("5 + 6;", 5, "+", 6),
            ("5 - 5;", 5, "-", 5),
            ("5 * 5;", 5, "*", 5),
            ("5 / 5;", 5, "/", 5),
            ("5 > 5;", 5, ">", 5),
            ("5 < 5;", 5, "<", 5),
            ("5 == 5;", 5, "==", 5),
            ("5 != 5;", 5, "!=", 5),
            ("true == true", True, "==", True),
            ("true != false", True, "!=", False),
            ("false == false", False, "==", False),
        ]

        for test in infix_tests:
            l = Lexer(test[0])
            p = Parser(l)
            program = p.parse_program()

            assert len(program.statements) == 1
            
            stmt: AST.ExpressionStatement = program.statements[0]
            exp: AST.InfixExpression = stmt.expression
            assert self.test_integer_literal(exp.left, test[1])

            assert exp.operator == test[2]
            assert self.test_integer_literal(exp.right, test[3])

            if not self.test_infix_expression(exp, test[1], test[2], test[3]):
                return

    def test_parsing_operator_precedence(self):
        infix_tests = [
            # input, left_value, operator, right_value
            ("-a * b", "((-a) * b)"),
            ("!-a", "(!(-a))"),
            ("a + b + c", "((a + b) + c)"),
            ("a + b -c", "((a + b) - c)"),
            ("a * b + c", "((a * b) + c)"),
            ("a * b / c", "((a * b) / c)"),
            ("a + b / c", "(a + (b / c))"),
            ("a + b * c + d / e - f", 
                "(((a + (b * c)) + (d / e)) - f)"),
            ("3 + 4; -5 * 5",
                "(3 + 4)((-5) * 5)"),
            ("5 > 4 == 3 < 4",
                "((5 > 4) == (3 < 4))"),
            ("5 < 4 != 3 > 4",
                "((5 < 4) != (3 > 4))"),
            ("3 + 4 * 5 == 3 * 1 + 4 * 5",
                "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))"),
            ("true", "true"),
            ("false", "false"),
            ("3 > 5 == false", "((3 > 5) == false)"),
            ("3 < 5 == true", "((3 < 5) == true)"),
            (
                "1 + (2 + 3) + 4",
                "((1 + (2 + 3)) + 4)",
            ),
            (
                "(5 + 5) * 2",
                "((5 + 5) * 2)",
            ),
            (
                "2 / (5 + 5)",
                "(2 / (5 + 5))",
            ),
            (
                "-(5 + 5)",
                "(-(5 + 5))",
            ),
            (
                "!(true == true)",
                "(!(true == true))",
            ),
            (
                "a + add(b * c) + d",
                "((a + add((b * c))) + d)",
            ),
            (
                "add(a, b, 1, 2 * 3, 4 + 5, add(6, 7 * 8))",
                "add(a, b, 1, (2 * 3), (4 + 5), add(6, (7 * 8)))",
            ),
            (
                "add(a + b + c * d / f + g)",
                "add((((a + b) + ((c * d) / f)) + g))",
            ),
        ]

        for test in infix_tests:
            l = Lexer(test[0])
            p = Parser(l)
            program = p.parse_program()
            
            assert str(program) == test[1]

    def test_if_expression(self):
        input = 'if (x < y) { u }'

        l = Lexer(input)
        p = Parser(l)
        program = p.parse_program()

        assert len(program.statements) == 1
        exp: AST.IfExpression = program.statements[0].expression
        self.test_infix_expression(exp.condition, "x", "<", "y")

        consequence: AST.ExpressionStatement = exp.consequence.statements[0]
        self.test_identifier(consequence.expression, "x")
        assert exp.alternative == None

    def test_function_literal_parsing(self):
        input = 'fn(x, y) { x + y; }'

        l = Lexer(input)
        p = Parser(l)
        program = p.parse_program()

        assert len(program.statements) == 1
        exp: AST.FunctionLiteral = program.statements[0].expression

        assert len(exp.parameters) == 2
        self.test_literal_expression(exp.parameters[0], "x")
        self.test_literal_expression(exp.parameters[1], "y")

        assert len(exp.body.statements) == 1
        body_stmt = exp.body.statements[0]
        self.test_infix_expression(body_stmt.expression, "x", "+", "y")

    def test_call_expression_parsing(self):
        input = 'add(1, 2 * 3, 4 + 5);'

        l = Lexer(input)
        p = Parser(l)
        program = p.parse_program()

        assert len(program.statements) == 1
        exp: AST.CallExpression = program.statements[0].expression

        assert self.test_identifier(exp.function, "add")
        assert len(exp.arguments) == 3
        assert self.test_literal_expression(exp.arguments[0], 1)
        assert self.test_infix_expression(exp.arguments[1], 2, "*", 3)
        assert self.test_infix_expression(exp.arguments[2], 4, "+", 5)

    @pytest.mark.skip(reason="Don't test helper function")
    def test_integer_literal(self, exp: AST.Expression, value: int):
        integer: AST.IntegerLiteral = exp
        if integer.value != value:
            return False
        if integer.token_literal() != str(value).lower():
            return False
        return True

    @pytest.mark.skip(reason="Don't test helper function")
    def test_identifier(self, exp: AST.Expression, value: str):
        ident = exp
        if ident.value != value:
            return False
        if ident.token_literal() != value:
            return False
        return True

    @pytest.mark.skip(reason="Don't test helper function")
    def test_literal_expression(self, exp: AST.Expression, value: str):
        if value in ('true', 'false'):
            return self.test_boolean_literal(exp, value == 'true')
        elif isinstance(value, int) or value.isnumeric():
            return self.test_integer_literal(exp, int(value))
        else:
            return self.test_identifier(exp, value)

    @pytest.mark.skip(reason="Don't test helper function")
    def test_infix_expression(self, exp: AST.Expression, left: any, operator: str, right: any):
        if not self.test_literal_expression(exp.left, left):
            return False

        if not exp.operator == operator:
            return False

        if not self.test_literal_expression(exp.right, right):
            return False

        return True

    @pytest.mark.skip(reason="Don't test helper function")
    def test_boolean_literal(self, exp: AST.Expression, value: bool) -> bool:
        boolean: AST.Boolean = exp

        if boolean.value != value:
            return False

        if boolean.token_literal() != ('True' if value else 'false'):
            return False

        return True
