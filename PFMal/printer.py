from mal_types import MalType, Symbol, String, Number, Nil, Sexpr, BoolFalse, BoolTrue, Vector, SpliceUnQuote, \
    UnQuote, QuasiQuote, Quote, Deref, HashMap


def pr_str(mal_object: MalType, print_readably: bool = True) -> str:
    type_to_function = {
        Number: lambda mal_obj: str(mal_obj),
        Sexpr: lambda mal_sexpr: f'({" ".join([pr_str(mal_obj) for mal_obj in mal_sexpr])})',
        Vector: lambda mal_sexpr: f'[{" ".join([pr_str(mal_obj) for mal_obj in mal_sexpr])}]',
        HashMap: lambda mal_sexpr: f'{{{" ".join([f"{pr_str(k)} {pr_str(v)}" for (k,v) in mal_sexpr.items()])}}}',
        String: lambda mal_obj: mal_obj.__str__(print_readably),
        BoolTrue: lambda _: 'true',
        BoolFalse: lambda _: 'false',
        Nil: lambda _: 'nil',
        Symbol: lambda mal_obj: str(mal_obj),
        Quote: lambda _: 'quote',
        QuasiQuote: lambda _: 'quasiquote',
        UnQuote: lambda _: 'unquote',
        SpliceUnQuote: lambda _: 'splice-unquote',
        Deref: lambda _: 'deref',
    }

    return type_to_function[type(mal_object)](mal_object)
