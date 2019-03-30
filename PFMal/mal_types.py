class MalType:
    pass


class Number(int, MalType):
    pass


class Symbol(str, MalType):
    pass


class Nil(MalType):
    pass


class Bool(bool, MalType):
    pass


class String(str, MalType):
    pass
