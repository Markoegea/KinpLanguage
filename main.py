import sys
from kp.repl import (loop_evaluator, file_evaluator)
#Para usar los test "mypy . && nosetests"

def main() -> None:
    print('Bienvenido al lenguaje de Programacion Kinp.')
    print('Escribe un comando para comenzar.')
    loop_evaluator()
         

if __name__ == '__main__':
    if (len(sys.argv) > 1):
        path = sys.argv[1]
        file_evaluator(path)
    else:
        main()