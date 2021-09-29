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
        elif isinstance(node, ast.InfixExpression):
            left = self.eval(node.left)
            right = self.eval(node.right)
            return self.eval_infix_expression(node.operator, left, right)
        elif isinstance(node, ast.IfExpression):
            condition = self.eval(node.condition)
            if condition not in [FALSE, NULL]:
                return self.eval(node.consequence)
            else:
                return self.eval(node.alternative)
        elif isinstance(node, ast.BlockStatement):
            return self.eval_statements(node.statements)
        elif isinstance(node, ast.ReturnStatement):
            val = self.eval(node.return_value)
            return objects.ReturnValue(val)

    def eval_statements(self, stmts: "list[ast.Statement]") -> Object:
        result = None

        for statement in stmts:
            result = self.eval(statement)

            if isinstance(result, objects.ReturnValue):
                return result.value

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

    def eval_infix_expression(self, operator: str, left: objects.Object, right: objects.Object) -> objects.Object:
        if left.type() == objects.INTEGER_OBJ or right.type() == objects.INTEGER_OBJ:
            return self.eval_integer_infix_expression(operator, left, right)
        elif operator == '==':
            return self.native_bool_to_boolean_object(left == right)
        elif operator == '!=':
            return self.native_bool_to_boolean_object(left != right)

    def eval_integer_infix_expression(self, operator: str, left: objects.Integer, right: objects.Integer) -> objects.Integer:
        left_val = left.value
        right_val = right.value

        if operator == '+':
            return objects.Integer(left_val + right_val)
        elif operator == '-':
            return objects.Integer(left_val - right_val)
        elif operator == '*':
            return objects.Integer(left_val * right_val)
        elif operator == '/':
            return objects.Integer(left_val / right_val)
        elif operator == '<':
            return self.native_bool_to_boolean_object(left_val < right_val)
        elif operator == '>':
            return self.native_bool_to_boolean_object(left_val > right_val)
        elif operator == '==':
            return self.native_bool_to_boolean_object(left_val == right_val)
        elif operator == '!=':
            return self.native_bool_to_boolean_object(left_val != right_val)
