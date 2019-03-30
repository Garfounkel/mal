from mal_readline import init_readline


def READ(inputs: str) -> str:
    return inputs


def EVAL(ast: str, env: dict) -> str:
    return ast


def PRINT(exp: str) -> str:
    return exp


def rep(inputs: str) -> str:
    return PRINT(EVAL(READ(inputs), {}))


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
