from mal_readline import init_readline


def READ(input_str: str) -> str:
    return input_str


def EVAL(ast: str, env: dict) -> str:
    return ast


def PRINT(exp: str) -> str:
    return exp


def rep(input_str: str) -> str:
    return PRINT(EVAL(READ(input_str), {}))


if __name__ == '__main__':
    init_readline()
    while True:
        try:
            print(rep(input('user> ')))
        except KeyboardInterrupt:
            print('^C')
        except EOFError:
            print()
            exit(0)
