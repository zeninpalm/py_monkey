class Environment:
    def __init__(self, outer: "Environment" = None) -> None:
        self.store : dict[str, "Object"] = {}
        if not outer:
            self.outer = None
        else:
            self.outer = outer 

    def get(self, name: str) -> "Object":
        obj = self.store.get(name)
        if not obj and self.outer:
            obj = self.outer.get(name)

        return obj

    def set(self, name: str, val: "Object") -> None:
        self.store[name] = val
        return val
