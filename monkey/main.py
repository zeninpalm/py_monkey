from lexer import Lexer

input = '=+{}'
lexer = Lexer(input)

print(lexer.next_token())
print(lexer.next_token())
print(lexer.next_token())
