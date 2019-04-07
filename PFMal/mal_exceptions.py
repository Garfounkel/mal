class MalError(Exception):
    pass


class MalParseError(MalError):
    pass


class BlankInput(Exception):
    pass


class SymbolNotFound(MalError):
    pass
