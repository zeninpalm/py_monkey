INTEGER_OBJ = "INTEGER"
BOOLEAN_OBJ = "BOOLEAN"
NULL_OBJ = "NULL"


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
