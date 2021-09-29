from . import ast
from . import objects
from .objects import Object


TRUE = objects.Boolean(True)
FALSE = objects.Boolean(False)
NULL = objects.Null()

class Evaluator:
    def eval(self, node: ast.Node) -> Object:
        if isinstance(node, ast.Program):
            return self.eval_statements(node.statements)
        elif isinstance(node, ast.ExpressionStatement):
            return self.eval(node.expression)
        elif isinstance(node, ast.IntegerLiteral):
            return objects.Integer(node.value)
        elif isinstance(node, ast.Boolean):
            return self.native_bool_to_boolean_object(node.value)
        elif isinstance(node, ast.PrefixExpression):
            right = self.eval(node.right)
            return self.eval_prefix_expression(node.operator, right)

    def eval_statements(self, stmts: "list[ast.Statement]") -> Object:
        result: Object = None

        for statement in stmts:
            result = self.eval(statement)

        return result

    def eval_prefix_expression(self, operator: str, right: objects.Object) -> objects.Object:
        if operator == '!':
            return self.eval_bang_operator_expression(right)
        elif operator == '-':
            return self.eval_minus_prefix_operator_expression(right)

    def native_bool_to_boolean_object(self, value: bool) -> objects.Boolean:
        if value:
            return TRUE
        else:
            return FALSE

    def eval_bang_operator_expression(self, right: objects.Object) -> objects.Object:
        if right == TRUE:
            return FALSE
        elif right == FALSE:
            return TRUE
        elif right == NULL:
            return TRUE
        else:
            return FALSE

    def eval_minus_prefix_operator_expression(self, right: objects.Object) -> objects.Object:
        if right.type() != objects.INTEGER_OBJ:
            return None

        return objects.Integer(right.value)
