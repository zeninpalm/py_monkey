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



if __name__ == '__main__':
    test_let_statements()