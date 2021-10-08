from .objects import Object


class Environment:
    def __init__(self) -> None:
        self.store : dict[str, Object] = {}

    def get(self, name: str) -> Object:
        return self.store.get(name)

    def set(self, name: str, val: Object) -> None:
        self.store[name] = val
        return val
