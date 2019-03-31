class MalType:
    pass


class Number(int, MalType):
    pass


class Symbol(str, MalType):
    pass


class Nil(MalType):
    pass


class BoolTrue(MalType):
    pass


class BoolFalse(MalType):
    pass


class String(str, MalType):
    pass


class Sexpr(list, MalType):
    pass


class Vector(list, MalType):
    pass
