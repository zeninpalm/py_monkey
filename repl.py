import sys

from monkey.lexer import Lexer
from monkey.parser import Parser
from monkey.token import Token, TokenType

PROMPT = '>> '

def start():
    while True:
        line = input(PROMPT)
        if 'q' == line.rstrip():
            break
        lexer = Lexer(line)
        parser = Parser(lexer)
        program = parser.parse_program()
        print(f'{program}\n')

if __name__ == '__main__':
    start()
