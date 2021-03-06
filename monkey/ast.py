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


class StringLiteral(Expression):
    def __init__(self, token: Token, value: str) -> None:
        self.token = token
        self.value = value

    def expression_node(self):
        return None

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return self.token.literal


class Identifier(Expression):
    def __init__(self, token: Token, value: str) -> None:
        self.token = token
        self.value = value
    
    def expression_Node(self) -> Node:
        return None

    def token_literal(self) -> str:
        return self.token.literal
    
    def __str__(self):
        return self.value

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


class IntegerLiteral(Expression):
    def __init__(self, token: Token, value: int):
        self.token = token
        self.value = value

    def expression_node(self):
        return None

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return self.token.literal


class PrefixExpression(Expression):
    def __init__(self, token: Token, operator: str, right: Expression):
        self.token = token
        self.operator = operator
        self.right = right

    def expression_node(self):
        return None

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"({self.operator}{self.right})"

class InfixExpression(Expression):
    def __init__(self, token: Token, left: Expression, operator: str, right: Expression = None):
        self.token = token
        self.operator = operator
        self.right = right
        self.left = left

    def expression_node(self):
        return None

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"({self.left} {self.operator} {self.right})"

class Boolean(Expression):
    def __init__(self, token: Token, value: bool):
        self.token = token
        self.value = value

    def expression_node(self):
        return None

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return self.token.literal


class BlockStatement(Statement):
    def __init__(self, token: Token, statements: "list[Statement]" = []):
        self.token = token
        self.statements = statements

    def statement_node(self):
        return None

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        out = ''
        for s in self.statements:
            out += str(s)
        return out

class IfExpression(Expression):
    def __init__(self, token: Token, condition: Expression, consequence: BlockStatement, alternative: BlockStatement = None):
        self.token = token
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def expression_node(self):
        return None

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        out = 'if '
        out += str(self.condition)
        out += ' '
        out += str(self.consequence)

        if not self.alternative:
            out += ' else '
            out += str(self.alternative)

        return out

class FunctionLiteral(Expression):
    def __init__(self, token: Token, parameters: "list[Identifier]" = [], body: BlockStatement = None):
        self.token = token
        self.parameters = parameters
        self.body = body

    def expression_node(self):
        return None

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self):
        params: list[str] = []
        for p in self.parameters:
            params.append(str(p))

        return f"{self.token_literal()} ({', '.join(params)}) {{ {str(self.body)} }}"

class CallExpression(Expression):
    def __init__(self, token: Token, function: Expression, arguments: "list[Expression]") -> None:
        self.token = token
        self.function = function
        self.arguments = arguments

    def expression_node(self):
        return None

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        args = []
        for a in self.arguments:
            args.append(str(a))

        return f"{self.function}({', '.join(args)})"
