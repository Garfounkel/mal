def READ(inputs: str) -> str:
    return inputs


def EVAL(ast) -> str:  # TODO: Add correct type
    return ast


def PRINT(inputs: str) -> str:
    return inputs


def rep(inputs: str) -> str:
    return PRINT(EVAL(READ(inputs)))


if __name__ == '__main__':
    while True:
        try:
            user_input = input('user> ')
            output = rep(user_input)
            print(output)
        except EOFError:
            print()
            exit(0)
