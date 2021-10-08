import string

from .token import TokenType, Token, lookup_ident

class Lexer:
    def __init__(self, input: str = ""):
        self._input = input
        self._position = 0
        self._read_position = 0
        self._ch = None

        self.read_char()

    def read_char(self) -> str:
        if self._read_position >= len(self._input):
            self._ch = None
        else:
            self._ch = self._input[self._read_position]

        self._position = self._read_position
        self._read_position += 1

    def __str__(self) -> str:
        return f"Lexer('{self._input}' : {self._ch})@({self._position}, {self._read_position})"

    def next_token(self) -> Token:
        token = None

        self.skip_whitespace()

        if self._ch == '=':
            if self.peek_char() == '=':
                self.read_char()
                token = Token(TokenType.EQ, '==')
            else:
                token = Token(TokenType.ASSIGN, self._ch)
        elif self._ch == ';':
            token = Token(TokenType.SEMICOLON, self._ch)
        elif self._ch == '(':
            token = Token(TokenType.LPAREN, self._ch)
        elif self._ch == ')':
            token = Token(TokenType.RPAREN, self._ch)
        elif self._ch == '{':
            token = Token(TokenType.LBRACE, self._ch)
        elif self._ch == '}':
            token = Token(TokenType.RBRACE, self._ch)
        elif self._ch == ',':
            token = Token(TokenType.COMMA, self._ch)
        elif self._ch == '+':
            token = Token(TokenType.PLUS, self._ch)
        elif self._ch == '-':
            token = Token(TokenType.MINUS, self._ch)
        elif self._ch == '!':
            if self.peek_char() == '=':
                self.read_char()
                token = Token(TokenType.NOT_EQ, '!=')
            else:
                token = Token(TokenType.BANG, self._ch)
        elif self._ch == '/':
            token = Token(TokenType.SLASH, self._ch)
        elif self._ch == '*':
            token = Token(TokenType.ASTERISK, self._ch)
        elif self._ch == '<':
            token = Token(TokenType.LT, self._ch)
        elif self._ch == '>':
            token = Token(TokenType.GT, self._ch)
        elif self._ch == None:
            token = Token(TokenType.EOF, self._ch)
        elif self._ch == '"':
            token = Token(TokenType.STRING, self.read_string())
        else:
            if self.is_letter(self._ch):
                literal = self.read_identifier()
                token = Token(lookup_ident(literal), literal)
                return token
            elif self._ch in string.digits:
                token = Token(TokenType.INT, self.read_number())
                return token
            else:
                return Token(TokenType.ILLEGAL, self._ch)
        self.read_char()
        return token
    
    def skip_whitespace(self):
        while self._ch and (self._ch in string.whitespace):
            self.read_char()

    def is_letter(self, character: str) -> bool:
        return self._ch and ((character in string.ascii_letters) or (character == '_'))

    def read_identifier(self) -> str:
        position = self._position
        while self.is_letter(self._ch):
            self.read_char()

        return self._input[position:self._position]

    def read_number(self) -> str:
        position = self._position
        while self._ch and (self._ch in string.digits):
            self.read_char()

        return self._input[position:self._position]

    def peek_char(self) -> str:
        if self._read_position >= len(self._input):
            return None
        else:
            return self._input[self._read_position]

    def read_string(self) -> str:
        position = self._position + 1

        while True:
            self.read_char()
            if self._ch == '"' or not self._ch:
                break
        
        return self._input[position:self._position]
