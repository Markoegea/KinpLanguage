from typing import (cast, Dict)

from kp.object import (
    Error,
    Object,
    String,
    Integer,
    Builtin,
    Null,
)
_WRONG_NUMBER_OF_ARGS= 'Poseemos un problema, numero incorrecto de argumentos, se requeria {}, pero se recibio {}'
_UNSUPPORTED_ARGUMENT_TYPE= 'Poseemos un problema, no tengo soporte para {}'

def longitud(*args: Object) -> Object:
    if len(args) != 1:
        return Error(_WRONG_NUMBER_OF_ARGS.format(1,len(args)))
    elif type(args[0]) == String:
        argument = cast(String , args[0])
        string_len = len(argument.value)
        return Integer(string_len)
    else:
        return Error(_UNSUPPORTED_ARGUMENT_TYPE.format(args[0].type().name))

def imprimir(*args: Object) -> Object:
    if len(args) != 1:
        return Error(_WRONG_NUMBER_OF_ARGS.format(1,len(args)))
    else:
        print(args[0].inspect())
        return Null()


BUILTINS: Dict[str, Builtin] = {
    'longitud' : Builtin(fn=longitud),
    'imprimir' : Builtin(fn=imprimir),
}