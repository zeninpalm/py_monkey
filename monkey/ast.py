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

    def __str__(self) -> str:
        out = ''
        for s in self.statements:
            out += str(s)
        return out

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


class ReturnStatement(Statement):
    def __init__(self, token: Token, return_value: Expression = None):
        self.token = token
        self.return_value = return_value

    def statement_node(self) -> Node:
        return None

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"{self.token_literal()} {str(self.return_value)}"


class ExpressionStatement(Statement):
    def __init__(self, token: Token = None, expression: Expression = None):
        self.token = token
        self.expression = expression

    def statement_node(self):
        return None

    def token_literal(self) -> str:
        return self.token.token_literal()

    def __str__(self) -> str:
        if self.expression:
            return str(self.expression)

        return ''
