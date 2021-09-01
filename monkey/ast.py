from .token import Token


class Node:
    def token_literal(self) -> str:
        raise NotImplementedError()

class Statement(Node):
    def statement_node(self) -> str:
        raise NotImplementedError()

class Expression(Node):
    def expression_node(self) -> str:
        raise NotImplementedError()

class Program(Node):
    def __init__(self):
        self.statements: list[Statement] = []

    def token_literal(self) -> str:
        if self.statements:
            return self.statements[0].token_literal()
        else:
            return ''

class Identifier(Expression):
    def __init__(self, token: Token, value: str) -> None:
        self.token = token
        self.value = value
    
    def expression_Node(self) -> Node:
        return None

    def token_literal(self) -> str:
        return self.token.literal

class LetStatement(Statement):
    def __init__(self, token: Token, identifier: Identifier, value: Expression):
        self.token = token
        self.name = identifier
        self.value = value

    def statement_node(self) -> Node:
        return None

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self):
        return f"LetStatement: {self.token} - {self.name.token_literal()} - {self.value}"
