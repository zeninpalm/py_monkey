from logging import ERROR


INTEGER_OBJ = "INTEGER"
BOOLEAN_OBJ = "BOOLEAN"
NULL_OBJ = "NULL"
RETURN_VALUE_OBJ = "RETURN_VALUE"
ERROR_OBJ = "ERROR"


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
