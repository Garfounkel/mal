import re
from mal_exceptions import MalParseError, BlankInput
from mal_types import MalType, Number, Symbol, Nil, String, Sexpr, BoolTrue, BoolFalse, Vector, Quote, QuasiQuote, \
    UnQuote, SpliceUnQuote, Deref, HashMap
from typing import Union


class Reader:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = 0

    def next(self) -> str:
        tok = self.peek()
        self.pos += 1
        return tok

    def peek(self) -> str:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None


def tokenize(input_str: str) -> list:
    pattern = re.compile(r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`@,;]+)""")
    return [tok for tok in pattern.findall(input_str) if tok[0] != ';']


def read_sequence(reader: Reader, start='(', end=')') -> Union[Sexpr, Vector]:
    reader.next()  # skips the opening paren '('
    sequence = Sexpr() if start == '(' else Vector()

    while True:
        tok = reader.peek()
        if tok is None:
            raise MalParseError(f"Expected '{end}', got EOF")
        elif tok[0] != end:
            sequence.append(read_from(reader))
        else:
            break

    reader.next()  # skips the closing paren ')'
    return sequence


def read_atom(reader: Reader) -> MalType:
    token = reader.next()

    parse_keyword_scalars = {
        'nil': Nil(),
        'true': BoolTrue(),
        'false': BoolFalse(),
    }

    if token in parse_keyword_scalars:
        return parse_keyword_scalars[token]
    elif token[0] == '"':
        if token[-1] == '"':
            return String(token)
        else:
            raise MalParseError(f"Expected '\"', got EOF")
    else:
        try:
            parsed_integer = int(token)
            return Number(parsed_integer)
        except ValueError:
            return Symbol(token)


def read_hashmap(reader: Reader) -> MalType:
    elements = read_sequence(reader, start='{', end='}')
    if len(elements) % 2 != 0:
        raise MalParseError("Expected 'expr', got '}' (odd number of elements in hashmap)")
    return HashMap(elements)


def read_readermacros(reader: Reader) -> MalType:
    readermacro = {
        "'": Quote(),
        "`": QuasiQuote(),
        "~": UnQuote(),
        "~@": SpliceUnQuote(),
        "@": Deref()
    }[reader.next()]

    return Sexpr([readermacro, read_from(reader)])


def read_metadata(reader: Reader) -> MalType:
    reader.next()
    metadata = read_from(reader)
    expr = read_from(reader)
    return Sexpr([Symbol('with-meta'), expr, metadata])  # Todo: replace Symbol by Function


def read_from(reader: Reader) -> MalType:
    tok = reader.peek()
    if tok is None:
        raise BlankInput()
    elif tok[0] == '(':
        return read_sequence(reader, start='(', end=')')
    elif tok[0] == '[':
        return read_sequence(reader, start='[', end=']')
    elif tok[0] == '{':
        return read_hashmap(reader)
    elif tok.startswith(("'", "`", "~", "~@", "@")):
        return read_readermacros(reader)
    elif tok[0] == '^':
        return read_metadata(reader)
    else:
        return read_atom(reader)


def read_str(input_str) -> MalType:
    tokens = tokenize(input_str)
    reader = Reader(tokens)
    return read_from(reader)
