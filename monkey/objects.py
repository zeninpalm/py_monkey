from logging import ERROR
from monkey import ast
from monkey.environment import Environment


INTEGER_OBJ = "INTEGER"
BOOLEAN_OBJ = "BOOLEAN"
NULL_OBJ = "NULL"
RETURN_VALUE_OBJ = "RETURN_VALUE"
ERROR_OBJ = "ERROR"
FUNCTION_OBJ = "FUNCTION"
STRING_OBJ = "STRING"


class Object:
    def type(self) -> str:
        pass

    def inspect(self) -> str:
        pass


class Integer:
    def __init__(self, value: int) -> None:
        self.value = value

    def inspect(self) -> str:
        return f"{self.value}"

    def type(self) -> str:
        return INTEGER_OBJ


class Boolean:
    def __init__(self, value: bool) -> None:
        self.value = value

    def inspect(self) -> str:
        return f"{self.value}"

    def type(self) -> str:
        return BOOLEAN_OBJ


class Null:
    def type(self) -> str:
        return NULL_OBJ

    def inspect(self) -> str:
        return "null"


class ReturnValue:
    def __init__(self, value: Object) -> None:
        self.value = value

    def type(self) -> str:
        return RETURN_VALUE_OBJ

    def inspect(self) -> str:
        return self.value.inspect()

class Error:
    def __init__(self, message: str) -> None:
        self.message = message

    def type(self) -> str:
        return ERROR_OBJ

    def inspect(self) -> str:
        return "ERROR: " + self.message

class Function:
    def __init__(self, parameters: "list[ast.Identifier]" = [], body: ast.BlockStatement = None, env: Environment = None) -> None:
        self.parameters = parameters
        self.body = body
        self.env = env

    def type(self) -> str:
        return FUNCTION_OBJ

    def inspect(self) -> str:
        parameters = []
        for p in self.parameters:
            parameters.append(p)

        return f"fn({', '.join(parameters)} {{\n{self.body}\n}}"


class String:
    def __init__(self, value: str) -> None:
        self.value = value

    def type(self) -> str:
        return STRING_OBJ

    def inspect(self) -> str:
        return self.value
