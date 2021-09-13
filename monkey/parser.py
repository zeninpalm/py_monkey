from . import ast
from .ast import Program, ReturnStatement, Statement, LetStatement, Identifier
from .lexer import Lexer
from .token import Token, TokenType

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.cur_token: Token = None
        self.peek_token: Token = None

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
            return None

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