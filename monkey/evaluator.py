from . import ast
from . import objects
from .objects import Object


class Evaluator:
    def eval(self, node: ast.Node) -> Object:
        if isinstance(node, ast.Program):
            return self.eval_statements(node.statements)
        elif isinstance(node, ast.ExpressionStatement):
            return self.eval(node.expression)
        elif isinstance(node, ast.IntegerLiteral):
            return objects.Integer(node.value)

    def eval_statements(self, stmts: "list[ast.Statement]") -> Object:
        result: Object = None

        for statement in stmts:
            result = self.eval(statement)

        return result
