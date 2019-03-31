import sys
import traceback

from mal_exceptions import MalParseError, BlankInput
from mal_readline import init_readline
from mal_types import MalType
from printer import pr_str
from reader import read_str


def READ(input_str: str) -> MalType:
    return read_str(input_str)


def EVAL(ast: MalType, env: dict) -> MalType:
    return ast


def PRINT(exp: MalType) -> str:
    return pr_str(exp)


def rep(input_str: str) -> str:
    return PRINT(EVAL(READ(input_str), {}))


if __name__ == '__main__':
    init_readline()
    while True:
        try:
            print(rep(input('user> ')))
        except MalParseError as e:
            print("".join(traceback.format_exception(*sys.exc_info())))
        except BlankInput:
            continue
        except KeyboardInterrupt:
            print('^C')
        except EOFError:
            print()
            exit(0)
