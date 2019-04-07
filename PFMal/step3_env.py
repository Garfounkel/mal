import sys
import traceback

from env import Env, repl_env
from mal_exceptions import BlankInput, SymbolNotFound, MalError
from mal_readline import init_readline
from mal_types import MalType, Sexpr, Symbol, pytype_to_maltype, Vector, HashMap
from printer import pr_str
from reader import read_str


def eval_ast(ast: MalType, env: Env):
    if type(ast) is Symbol:
        return env.get(ast)
    elif type(ast) is Sexpr or type(ast) is Vector:
        evaluated = [EVAL(el, env) for el in ast]
        return type(ast)(evaluated)
    elif type(ast) is HashMap:
        return HashMap({k: EVAL(v, env) for k, v in ast.items()})
    else:
        return ast


def READ(input_str: str) -> MalType:
    return read_str(input_str)


def EVAL(ast: MalType, env: Env) -> MalType:
    if type(ast) is Sexpr:
        if len(ast) == 0:
            return ast
        else:
            if ast[0] == 'def!':
                val = EVAL(ast[2], env)
                env.set(ast[1], val)
                return val
            elif ast[0] == 'let*':
                let_env = Env(outer=env)
                for (k, v) in zip(*([iter(ast[1])] * 2)):
                    let_env.set(k, EVAL(v, let_env))
                return EVAL(ast[2], let_env)
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
