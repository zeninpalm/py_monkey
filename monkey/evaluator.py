from . import ast
from . import objects
from .objects import Object


class Evaluator:
    def eval(self, node: ast.Node) -> Object:
        for stmt in node.statements:
            if isinstance(stmt.expression, ast.IntegerLiteral):
                return objects.Integer(stmt.expression.value)