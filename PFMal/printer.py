from mal_types import MalType, Symbol, String, Number, Nil, Sexpr, BoolFalse, BoolTrue, Vector


def pr_str(mal_object: MalType) -> str:
    type_to_function = {
        Symbol: lambda mal_obj: mal_obj,
        Number: lambda mal_obj: str(mal_obj),
        Sexpr: lambda mal_sexpr: f'({" ".join([pr_str(mal_obj) for mal_obj in mal_sexpr])})',
        Vector: lambda mal_sexpr: f'[{" ".join([pr_str(mal_obj) for mal_obj in mal_sexpr])}]',
        String: lambda mal_obj: mal_obj,
        BoolTrue: lambda _: 'true',
        BoolFalse: lambda _: 'false',
        Nil: lambda _: 'nil',
    }

    return type_to_function[type(mal_object)](mal_object)
