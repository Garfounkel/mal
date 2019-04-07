import sys
import traceback

from mal_exceptions import BlankInput, SymbolNotFound, MalError
from mal_readline import init_readline
from mal_types import MalType, Sexpr, Symbol, pytype_to_maltype, Vector, HashMap
from printer import pr_str
from reader import read_str

repl_env = {'+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: int(a / b)}


def eval_ast(ast: MalType, env: dict):
    if type(ast) is Symbol:
        if ast in env:
            return env[ast]
        else:
            raise SymbolNotFound(f"'{ast}' not found.")
    elif type(ast) is Sexpr or type(ast) is Vector:
        evaluated = [EVAL(el, env) for el in ast]
        return type(ast)(evaluated)
    elif type(ast) is HashMap:
        return HashMap({k: EVAL(v, env) for k, v in ast.items()})
    else:
        return ast


def READ(input_str: str) -> MalType:
    return read_str(input_str)


def EVAL(ast: MalType, env: dict) -> MalType:
    if type(ast) is Sexpr:
        if len(ast) == 0:
            return ast
        else:
            evaluated_list = eval_ast(ast, env)
            result = evaluated_list[0](*evaluated_list[1:])
            return pytype_to_maltype(result)
    else:
        return eval_ast(ast, env)


def PRINT(exp: MalType) -> str:
    return pr_str(exp, print_readably=True)


def rep(input_str: str) -> str:
    return PRINT(EVAL(READ(input_str), repl_env))


if __name__ == '__main__':
    init_readline()
    while True:
        try:
            print(rep(input('user> ')))
        except MalError as e:
            print("".join(traceback.format_exception(*sys.exc_info())))
        except BlankInput:
            continue
        except KeyboardInterrupt:
            print('^C')
        except EOFError:
            print()
            exit(0)
