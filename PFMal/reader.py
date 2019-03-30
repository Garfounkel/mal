import re
from mal_exceptions import MalParseError
from mal_types import MalType, Number, Symbol, Nil, String, Bool


class Reader:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = 0

    def next(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def peek(self):
        return self.tokens[self.pos]


def tokenize(inputs: str) -> list:
    pattern = re.compile(r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}('"`,;)]*)""")
    return re.findall(pattern)


def read_list(reader: Reader) -> list:
    reader.next()  # skips the opening paren '('
    tokens = list()

    try:
        while reader.peek()[0] != ')':
            tokens.append(read_from(reader))
    except IndexError:  # EOF
        raise MalParseError(f'Expected a closing paren for s-expr at position {reader.pos}.')

    reader.next()  # skips the closing paren ')'
    return tokens


def read_atom(reader: Reader) -> MalType:
    token = reader.next()

    parse_keyword_scalars = {
        'nil': Nil(),
        'true': Bool(True),
        'false': Bool(False)
    }

    if token in parse_keyword_scalars:
        return parse_keyword_scalars[token]
    elif token[0] == '"' and token[-1] == '"':
        return String(token)
    else:
        try:
            parsed_integer = int(token)
            return Number(parsed_integer)
        except ValueError:
            return Symbol(token)


def read_from(reader: Reader) -> list:
    if reader.peek()[0] == '(':
        return read_list(reader)
    else:
        return [read_atom(reader)]


def read_str(input_str):
    tokens = tokenize(input_str)
    reader = Reader(tokens)
    read_from(reader)
