from enum import IntEnum, auto
from typing import Callable

from . import ast
from .ast import Program, ReturnStatement, Statement, LetStatement, Identifier
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


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.cur_token: Token = None
        self.peek_token: Token = None
        self.prefix_parse_fns = {}
        self.infix_parse_fns = {}

        self.register_prefix(TokenType.IDENT, self.parse_identifier)

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
        return left_exp

    def parse_identifier(self) -> ast.Expression:
        return Identifier(self.cur_token, self.cur_token.literal)

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
