import pytest

import monkey.ast as AST
from monkey.lexer import Lexer
from monkey.parser import Parser
from monkey.token import Token, TokenType


def test_let_statements():
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
        assert match_let_statement(statement, tt)

def match_let_statement(stmt: AST.Statement, name: str) -> bool:
    assert stmt.token_literal() == "let"

    let_stmt: AST.LetStatement = stmt
    assert let_stmt.name.value == name
    assert let_stmt.name.token_literal() == name
    return True

def test_return_statements():
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

def test_identifier_expression():
    input = "foobar"

    l = Lexer(input)
    p = Parser(l)
    program = p.parse_program()
    assert len(program.statements) == 1

    stmt: AST.ExpressionStatement = program.statements[0]
    ident: AST.Identifier = stmt.expression
    assert ident.value == "foobar"
    assert ident.token_literal() == "foobar"

def test_integer_literal_expression():
    input = "5"

    l = Lexer(input)
    p = Parser(l)
    program = p.parse_program()
    assert len(program.statements) == 1

    stmt: AST.ExpressionStatement = program.statements[0]
    literal: AST.IntegerLiteral = stmt.expression
    assert literal.value == 5
    assert literal.token_literal() == "5"

def test_parsing_prefix_expressions():
    prefix_tests = [
        ("!5;", "!", 5),
        ("-15;", "-", 15),
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

def test_parsing_infix_expression():
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
    ]

    for test in infix_tests:
        l = Lexer(test[0])
        p = Parser(l)
        program = p.parse_program()

        assert len(program.statements) == 1
        
        stmt: AST.ExpressionStatement = program.statements[0]
        exp: AST.InfixExpression = stmt.expression
        assert test_integer_literal(exp.left, test[1])

        assert exp.operator == test[2]
        assert test_integer_literal(exp.right, test[3])

@pytest.mark.skip(reason="Don't test helper function")
def test_integer_literal(exp: AST.Expression, value: int):
    integer: AST.IntegerLiteral = exp
    if integer.value != value:
        return False
    if integer.token_literal() != str(value):
        return False
    return True

@pytest.mark.skip(reason="Don't test helper function")
def test_identifier(exp: AST.Expression, value: str):
    ident = exp.identifier
    if ident.value != value:
        return False
    if ident.token_literal() != value:
        return False
    return True

@pytest.mark.skip(reason="Don't test helper function")
def test_literal_expression(exp: AST.Expression, value: str):
    if value.isnumeric():
        return test_integer_literal_expression(exp, int(value))
    else:
        return test_identifier(exp, value)

@pytest.mark.skip(reason="Don't test helper function")
def test_infix_expression(exp: AST.Expression, left: any, operator: str, right: any):
    if not test_literal_expression(exp.left, left):
        return False

    if not exp.operator == operator:
        return False

    if not test_literal_expression(exp.right, right):
        return False

    return True


if __name__ == '__main__':
    test_let_statements()