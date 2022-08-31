from typing import (cast, Dict)

from kp.object import (
    Boolean,
    Error,
    Object,
    String,
    Integer,
    Builtin,
    Null,
)
_WRONG_NUMBER_OF_ARGS= 'Poseemos un problema, numero incorrecto de argumentos, se requeria {}, pero se recibio {}'
_UNSUPPORTED_ARGUMENT_TYPE= 'Poseemos un problema, no tengo soporte para {}'
_THAT_IS_NOT_A_NUMBER = 'Poseemos un problema, "{}" no es numero y no se puede castear'

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

def recibir(*args:Object) -> Object:
    if len(args) != 1:
        return Error(_WRONG_NUMBER_OF_ARGS.format(1,len(args)))
    elif type(args[0]) == String:
        argument = cast(String, args[0])
        message = argument.value
        input_data = input(message) 
        return String(input_data)
    else:
        return Error(_UNSUPPORTED_ARGUMENT_TYPE.format(args[0].type().name))

def parsearAentero(*args:Object) -> Object:
    if len(args) != 1:
        return Error(_WRONG_NUMBER_OF_ARGS.format(1,len(args)))
    elif type(args[0]) == String:
        dataString = cast(String, args[0])
        valueString = dataString.value
        try:
            return Integer(int(valueString))
        except:
            return Error(_THAT_IS_NOT_A_NUMBER.format(valueString))
    elif type(args[0]) == Boolean:
        dataBoolean = cast(Boolean, args[0])
        valueBoolean = dataBoolean.value
        if(valueBoolean):
            return Integer(1)
        else:
            return Integer(0)
    else:
        return Error(_UNSUPPORTED_ARGUMENT_TYPE.format(args[0].type().name))

def parsearAtexto(*args:Object) -> Object:
    if len(args) != 1:
        return Error(_WRONG_NUMBER_OF_ARGS.format(1,len(args)))
    elif type(args[0]) == Integer:
        dataInteger = cast(Integer, args[0])
        valueInteger = dataInteger.value
        return String(str(valueInteger))
    elif type(args[0]) == Boolean:
        dataBoolean = cast(Boolean, args[0])
        valueBoolean = dataBoolean.value
        if(valueBoolean):
            return String("verdadero")
        else:
            return String("falso")
    elif type(args[0]) == String:
        dataString = cast(String, args[0])
        valueString = dataString.value
        return String(valueString)
    else:
        return Error(_UNSUPPORTED_ARGUMENT_TYPE.format(args[0].type().name))

def parsearAbooleano(*args:Object) -> Object:
    if len(args) != 1:
        return Error(_WRONG_NUMBER_OF_ARGS.format(1,len(args)))
    elif type(args[0]) == Integer:
        dataInteger = cast(Integer, args[0])
        valueInteger = dataInteger.value
        if (valueInteger == 1):
            return Boolean(True)
        else:
            return Boolean(False)
        #TODO: parsear strings
    else:
        return Error(_UNSUPPORTED_ARGUMENT_TYPE.format(args[0].type().name))

BUILTINS: Dict[str, Builtin] = {
    'longitud' : Builtin(fn=longitud),
    'imprimir' : Builtin(fn=imprimir),
    'recibir' : Builtin(fn=recibir),
    'parsearAentero' : Builtin(fn=parsearAentero),
    'parsearAtexto' : Builtin(fn=parsearAtexto),
    'parsearAbooleano' : Builtin(fn=parsearAbooleano),
}