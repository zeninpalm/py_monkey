import cmd

from monkey.lexer import Lexer
from monkey.token import Token, TokenType

PROMPT = '>> '

def start():
    line = input(PROMPT)

    while line:
        lexer = Lexer(line)

        tok = lexer.next_token()
        while tok.token_type != TokenType.EOF:
            tok = lexer.next_token()

        line = input(PROMPT)

if __name__ == '__main__':
    start()
