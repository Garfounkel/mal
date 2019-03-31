import re
from mal_exceptions import MalParseError, BlankInput
from mal_types import MalType, Number, Symbol, Nil, String, Sexpr, BoolTrue, BoolFalse, Vector
from typing import Union


class Reader:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = 0

    def next(self):
        tok = self.peek()
        self.pos += 1
        return tok

    def peek(self):
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
        'false': BoolFalse()
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


def read_from(reader: Reader) -> MalType:
    tok = reader.peek()
    if tok is None:
        raise BlankInput()
    if tok[0] == '(':
        return read_sequence(reader, start='(', end=')')
    if tok[0] == '[':
        return read_sequence(reader, start='[', end=']')
    else:
        return read_atom(reader)


def read_str(input_str) -> MalType:
    tokens = tokenize(input_str)
    reader = Reader(tokens)
    return read_from(reader)
