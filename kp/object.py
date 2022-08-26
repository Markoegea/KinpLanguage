from abc import(ABC,abstractmethod)
from enum import(auto,Enum)

class ObjecType(Enum):
    BOOLEAN = auto()
    INTEGER = auto()
    RETURN = auto()
    NULL = auto()

class Object(ABC):
    
    @abstractmethod
    def type(self) -> ObjecType:
        pass

    @abstractmethod
    def inspect(self) -> str:
        pass

class Integer(Object):
    def __init__(self, value: int) -> None:
        self.value = value
    
    def type(self) -> ObjecType:
        return ObjecType.INTEGER

    def inspect(self) -> str:
        return str(self.value)

class Boolean(Object):
    def __init__(self, value: bool) -> None:
        self.value = value
    
    def type(self) -> ObjecType:
        return ObjecType.BOOLEAN

    def inspect(self) -> str:
        return 'verdadero' if self.value else 'falso'

class Return(Object):
    def __init__(self, value: Object) -> None:
        self.value = value

    def type(self) -> ObjecType:
        return ObjecType.RETURN

    def inspect(self) -> str:
        return self.value.inspect()

class Null(Object):

    def type(self) -> ObjecType:
        return ObjecType.NULL

    def inspect(self) -> str:
        return 'nulo'
