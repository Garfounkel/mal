import re


class MalType:
    pass


# Scalars
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
    def __str__(self, print_readably: bool = True):
        if print_readably:
            return super(String, self).__str__()

        replacements = {
            '\\"': '"',
            '\\n': '\n',
            '\\\\': '\\'
        }
        pattern = re.compile('|'.join(map(re.escape, replacements)))

        return pattern.sub(lambda match: replacements[match.group(0)], self)


# Sequences
class Sexpr(list, MalType):
    pass


class Vector(list, MalType):
    pass


class HashMap(dict, MalType):
    def __init__(self, elements):
        super(HashMap, self).__init__(zip(elements[0::2], elements[1::2]))


# ReaderMacros
class ReaderMacro(MalType):
    pass


class Quote(ReaderMacro):
    pass


class QuasiQuote(ReaderMacro):
    pass


class UnQuote(ReaderMacro):
    pass


class SpliceUnQuote(ReaderMacro):
    pass


class Deref(ReaderMacro):
    pass
