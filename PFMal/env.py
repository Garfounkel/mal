from mal_exceptions import SymbolNotFound
from mal_types import Symbol, MalType


class Env:
    def __init__(self, outer=None):
        self.outer = outer
        self.data = dict()

    def set(self, key: Symbol, value):
        self.data[key] = value

    def find(self, key: Symbol):
        if key in self.data:
            return self.data
        elif self.outer is not None:
            return self.outer.find(key)
        return None

    def get(self, key: Symbol):
        env = self.find(key)
        if env is None:
            raise SymbolNotFound(f"'{key}' not found.")
        return env[key]


repl_env = Env()
repl_env.set(Symbol('+'), lambda a, b: a + b)
repl_env.set(Symbol('-'), lambda a, b: a - b)
repl_env.set(Symbol('*'), lambda a, b: a * b)
repl_env.set(Symbol('/'), lambda a, b: int(a / b))
