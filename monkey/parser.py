from enum import IntEnum, auto
from typing import Callable

from . import ast
from .ast import PrefixExpression, Program, ReturnStatement, Statement, LetStatement, Identifier
from .lexer import Lexer
from .token import Token, TokenType

class Precedence(IntEnum):
    LOWEST=auto()
    EQUALS=auto()
    LESSGREATER=auto()
    SUM=auto()
    PRODUCT=auto()
    PREFIX=auto()
    CALL=auto()

PRECEDENCES = {
    TokenType.EQ: Precedence.EQUALS,
    TokenType.NOT_EQ: Precedence.EQUALS,
    TokenType.LT: Precedence.LESSGREATER,
    TokenType.GT: Precedence.LESSGREATER,
    TokenType.PLUS: Precedence.SUM,
    TokenType.MINUS: Precedence.SUM,
    TokenType.SLASH: Precedence.PRODUCT,
    TokenType.ASTERISK: Precedence.PRODUCT,
}

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.cur_token: Token = None
        self.peek_token: Token = None
        self.prefix_parse_fns = {}
        self.infix_parse_fns = {}

        self.register_prefix(TokenType.IDENT, self.parse_identifier)
        self.register_prefix(TokenType.INT, self.parse_integer_literal)
        self.register_prefix(TokenType.BANG, self.parse_prefix_expression)
        self.register_prefix(TokenType.MINUS, self.parse_prefix_expression)

        self.register_infix(TokenType.PLUS, self.parse_infix_expression)
        self.register_infix(TokenType.MINUS, self.parse_infix_expression)
        self.register_infix(TokenType.SLASH, self.parse_infix_expression)
        self.register_infix(TokenType.ASTERISK, self.parse_infix_expression)
        self.register_infix(TokenType.EQ, self.parse_infix_expression)
        self.register_infix(TokenType.NOT_EQ, self.parse_infix_expression)
        self.register_infix(TokenType.LT, self.parse_infix_expression)
        self.register_infix(TokenType.GT, self.parse_infix_expression)

        self.next_token()
        self.next_token()
    
    def next_token(self) -> None:
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()
    
    def parse_program(self) -> Program:
        program = Program()
        
        while self.cur_token.token_type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt is not None:
                program.statements.append(stmt)
            self.next_token()
        return program
    
    def parse_statement(self) -> Statement:
        if self.cur_token.token_type == TokenType.LET:
            return self.parse_let_statement()
        elif self.cur_token.token_type == TokenType.RETURN:
            return self.parse_return_statement()
        else:
            return self.parse_expression_statement()

    def parse_let_statement(self) -> LetStatement:
        stmt = LetStatement(self.cur_token, None, None)

        if not self.expect_peek(TokenType.IDENT):
            return None

        name = Identifier(self.cur_token, self.cur_token.literal)
        if not self.expect_peek(TokenType.ASSIGN):
            return None
        stmt.name = name
        
        while not self.cur_token_is(TokenType.SEMICOLON):
            self.next_token()
        
        return stmt

    def parse_return_statement(self) -> ReturnStatement:
        stmt = ast.ReturnStatement(self.cur_token)
        self.next_token()

        while not self.cur_token_is(TokenType.SEMICOLON):
            self.next_token()
        
        return stmt

    def parse_expression_statement(self) -> ast.ExpressionStatement:
        stmt = ast.ExpressionStatement(self.cur_token)
        stmt.expression = self.parse_expression(Precedence.LOWEST)

        if self.peek_token_is(TokenType.SEMICOLON):
            self.next_token()

        return stmt

    def parse_expression(self, precedence: int) -> ast.Expression:
        prefix = self.prefix_parse_fns[self.cur_token.token_type]
        if not prefix:
            return None
        left_exp = prefix()

        while not self.peek_token_is(TokenType.SEMICOLON) and precedence < self.peek_precedence():
            infix = self.infix_parse_fns.get(self.peek_token.token_type)
            if not infix:
                return left_exp
            self.next_token()
            left_exp = infix(left_exp)

        return left_exp

    def parse_prefix_expression(self) -> ast.Expression:
        token = self.cur_token
        operator = self.cur_token.literal
        self.next_token()

        return PrefixExpression(token, operator, self.parse_expression(Precedence.PREFIX))

    def parse_infix_expression(self, left: ast.Expression) -> ast.Expression:
        precedence = self.cur_precedence()
        exp = ast.InfixExpression(
            token=self.cur_token,
            operator=self.cur_token.literal,
            left=left
        )
        print(f"current token = {self.cur_token}")
        self.next_token()
        exp.right = self.parse_expression(precedence)
        return exp

    def parse_identifier(self) -> ast.Expression:
        return Identifier(self.cur_token, self.cur_token.literal)

    def parse_integer_literal(self) -> ast.Expression:
        value = int(self.cur_token.literal)
        return ast.IntegerLiteral(self.cur_token, value)

    def cur_token_is(self, t: TokenType) -> bool:
        return self.cur_token.token_type == t
    
    def peek_token_is(self, t: TokenType) -> bool:
        return self.peek_token.token_type == t
    
    def expect_peek(self, t: TokenType) -> bool:
        if self.peek_token_is(t):
            self.next_token()
            return True
        else:
            return False
    
    def register_prefix(self, token_type: TokenType, prefix_parse_fn: Callable):
        self.prefix_parse_fns[token_type] = prefix_parse_fn

    def register_infix(self, token_type: TokenType, infix_parse_fn: Callable):
        self.infix_parse_fns[token_type] = infix_parse_fn

    def peek_precedence(self) -> int:
        p = PRECEDENCES.get(self.peek_token.token_type)
        return p or Precedence.LOWEST

    def cur_precedence(self) -> int:
        p = PRECEDENCES.get(self.cur_token.token_type)
        return p or Precedence.LOWEST
