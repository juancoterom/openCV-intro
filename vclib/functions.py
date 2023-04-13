import cv2
import numpy as np
import random


def adivina(attempt: int) -> None:
    """Compares an input integer to a randomly generated value,
    given the amount of attempts.
    """

    number = random.randint(0, 100)
    print(f'Numero generado: {number}')

    for i in range(attempt):
        valid_guess = False
        while not valid_guess:
            try:
                guess = int(input(f'Intentos: {attempt - i}.'
                + 'Adivine numero entre 0 y 100: '))
                valid_guess = True
            except ValueError:
                print('ERROR: Debe ingresar un entero.')
        
        if guess == number:
            print(f'Ha adivinado en {i + 1} intentos.')
            return
    
    print('No ha adivinado.')


def thresh(img: list[list[int]]) -> list[list[int]]:
    """Returns thresholded image, given an input image."""

    def evaluate(pixel: int) -> int:
        """Evaluates a single pixel as either black or white."""

        return 0 if pixel < 220 else 255
    
    return [[evaluate(pixel) for pixel in row] for row in img]