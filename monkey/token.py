from enum import IntEnum, auto

class TokenType(IntEnum):
    ASSIGN=auto()
    LET=auto()
    INT=auto()
    ILLEGAL=auto()
    IDENT=auto()
    FUNCTION=auto()
    PLUS=auto()
    LPAREN=auto()
    RPAREN=auto()
    LBRACE=auto()
    RBRACE=auto()
    COMMA=auto()
    SEMICOLON=auto()
    EOF=auto()

keywords = {
    "fn": TokenType.FUNCTION,
    "let": TokenType.LET,
}

def lookup_ident(ident: str) -> TokenType:
    token_type = keywords.get(ident)
    if token_type:
        return token_type
    else:
        return TokenType.IDENT
    
class Token:
    def __init__(self, token_type, literal):
        self._token_type = token_type
        self._literal = literal

    @property
    def token_type(self):
        return self._token_type

    @property
    def literal(self):
        return self._literal

    def __str__(self):
        return f"Token {self._token_type}, {self._literal}"
