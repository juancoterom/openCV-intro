# OTERO, Juan Cruz - 71459
# TP01 - Funcion en Python

import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from vclib.functions import adivina


def main() -> None:
    # Input total amount of attempts.
    valid_attempt = False
    while not valid_attempt:
        try:
            attempt = int(input('Ingrese total de intentos: '))
            valid_attempt = True
        except ValueError:
            print('ERROR: Debe ingresar un entero.')
    
    # Function call.
    adivina(attempt)


if __name__ == '__main__':
    main()