from . import ast
from .object import Object

class Evaluator:
    @classmethod
    def eval(cls, node: ast.Node) -> Object:
        if isinstance(node, ast.IntegerLiteral):
            pass