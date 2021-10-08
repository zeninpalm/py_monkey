from inspect import unwrap
from . import ast
from . import objects
from .objects import Object
from .environment import Environment


TRUE = objects.Boolean(True)
FALSE = objects.Boolean(False)
NULL = objects.Null()


class Evaluator:
    def eval(self, node: ast.Node, env: Environment) -> Object:
        if isinstance(node, ast.Program):
            return self.eval_program(node, env)
        elif isinstance(node, ast.ExpressionStatement):
            return self.eval(node.expression, env)
        elif isinstance(node, ast.IntegerLiteral):
            return objects.Integer(node.value)
        elif isinstance(node, ast.Boolean):
            return self.native_bool_to_boolean_object(node.value)
        elif isinstance(node, ast.PrefixExpression):
            right = self.eval(node.right, env)
            if self.is_error(right):
                return right
            return self.eval_prefix_expression(node.operator, right)
        elif isinstance(node, ast.InfixExpression):
            left = self.eval(node.left, env)
            if self.is_error(left):
                return left

            right = self.eval(node.right, env)
            if self.is_error(right):
                return right

            return self.eval_infix_expression(node.operator, left, right)
        elif isinstance(node, ast.IfExpression):
            condition = self.eval(node.condition, env)
            if self.is_error(condition):
                return condition

            if condition not in [FALSE, NULL]:
                return self.eval(node.consequence, env)
            else:
                return self.eval(node.alternative, env)
        elif isinstance(node, ast.BlockStatement):
            return self.eval_block_statements(node, env)
        elif isinstance(node, ast.ReturnStatement):
            val = self.eval(node.return_value, env)
            if self.is_error(val):
                return val
            return objects.ReturnValue(val)
        elif isinstance(node, ast.LetStatement):
            val = self.eval(node.value, env)
            if self.is_error(val):
                return val
            else:
                env.set(node.name.value, val)
        elif isinstance(node, ast.Identifier):
            return self.eval_identifier(node, env)
        elif isinstance(node, ast.FunctionLiteral):
            params = node.parameters
            body = node.body
            return objects.Function(params, body, env)
        elif isinstance(node, ast.CallExpression):
            function = self.eval(node.function, env)
            if self.is_error(function):
                return function
            args = self.eval_expressions(node.arguments, env)
            if len(args) == 1 and self.is_error(args[0]):
                return args[0]
            return self.apply_function(function, args)

    def eval_program(self, program: ast.Program, env: Environment) -> Object:
        result = None
        for statement in program.statements:
            result = self.eval(statement, env)

            if isinstance(result, objects.ReturnValue):
                return result.value
            elif isinstance(result, objects.Error):
                return result

        return result

    def eval_block_statements(self, block: ast.BlockStatement, env: Environment) -> Object:
        result = None
        for statement in block.statements:
            result = self.eval(statement, env)

            if result:
                rt = result.type()
                if rt == objects.RETURN_VALUE_OBJ or rt == objects.ERROR_OBJ:
                    return result

        return result

    def eval_prefix_expression(self, operator: str, right: objects.Object) -> objects.Object:
        if operator == '!':
            return self.eval_bang_operator_expression(right)
        elif operator == '-':
            return self.eval_minus_prefix_operator_expression(right)
        else:
            return self.new_error(f"Unknown operator: {operator}{right.type()}")

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
            return self.new_error(f"Unknown operator: -{right.type()}")

        return objects.Integer(right.value)

    def eval_infix_expression(self, operator: str, left: objects.Object, right: objects.Object) -> objects.Object:
        if left.type() == objects.INTEGER_OBJ and right.type() == objects.INTEGER_OBJ:
            return self.eval_integer_infix_expression(operator, left, right)
        elif operator == '==':
            return self.native_bool_to_boolean_object(left == right)
        elif operator == '!=':
            return self.native_bool_to_boolean_object(left != right)
        elif left.type() != right.type():
            return self.new_error(f"Type mismatch: {left.type()} {operator} {right.type()}")
        else:
            return self.new_error(f"Unknown operator: {left.type()} {operator} {right.type()}")

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
        else:
            return self.new_error(f"Unknown operator: {left.type()} {operator} {right.type()}")

    def new_error(self, message: str) -> objects.Error:
        return objects.Error(message=message)

    def is_error(self, obj: objects.Object) -> bool:
        if obj:
            return obj.type() ==  objects.ERROR_OBJ
        return False

    def eval_identifier(self, node: ast.Identifier, env: Environment) -> objects.Object:
        val = env.get(node.value)
        if not val:
            return self.new_error(f"Identifier not found: {node.value}")
        return val

    def eval_expressions(self, exps: "list[ast.Expression]", env: Environment) -> "list[objects.Object]":
        result: list[objects.Object] = []

        for e in exps:
            evaluated = self.eval(e, env)
            if self.is_error(evaluated):
                return [evaluated]
            result.append(evaluated)
        
        return result

    def apply_function(self, fn: objects.Object, args: "list[objects.Object]") -> objects.Object:
        extended_env = self.extend_function_env(fn, args)
        evaluated = self.eval(fn.body, extended_env)
        return self.unwrap_return_value(evaluated)

    def extend_function_env(self, fn: objects.Function, args: "list[objects.Object]") -> Environment:
        env = Environment(fn.env)

        for index, param in enumerate(fn.parameters):
            env.set(param.value, args[index])

        return env

    def unwrap_return_value(self, obj: objects.Object) -> objects.Object:
        if isinstance(obj, objects.ReturnValue):
            return obj.value
        return obj
    
