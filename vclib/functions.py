import cv2
import cv2.aruco as aruco
import numpy as np
import random

from typing import List


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


def thresh(img: List[List[int]]) -> List[List[int]]:
    """Returns thresholded image, given an input image."""

    def evaluate(pixel: int) -> int:
        """Evaluates a single pixel as either black or white."""

        return 0 if pixel < 220 else 255
    
    return [[evaluate(pixel) for pixel in row] for row in img]


def similarity(
    imgCrop: List[List[int]], angle: int, tx: int, ty: int, scale: float=1
    ) -> List[List[int]]:
    """Applies rotation, scaling and translation to an image."""

    height, width = imgCrop.shape[:2]
    center = width/2, height/2
    matrixRot = cv2.getRotationMatrix2D(center, angle, scale)
    imgRot = cv2.warpAffine(imgCrop, matrixRot, (width, height))
    matrixTrans = np.float32([[1, 0, tx], [0, 1, ty]])
    imgSim = cv2.warpAffine(imgRot, matrixTrans, (width, height))
    return imgSim


def affine(
        img: List[List[int]], src: List[List[int]], des: List[List[int]]
        ) -> List[List[int]]:
    """Applies affine transformation to an image."""

    height, width = img.shape[:2]
    matrixAff = cv2.getAffineTransform(src, des)
    imgOut = cv2.warpAffine(img, matrixAff, (height, width))
    return imgOut


def rectify(
        img: List[List[int]], src: List[List[int]], des: List[List[int]]
        ) -> List[List[int]]:
    """Applies perspective transformation to an image."""

    height, width = img.shape[:2]
    matrixPersp = cv2.getPerspectiveTransform(src, des)
    imgOut = cv2.warpPerspective(img, matrixPersp, (height, width))
    return imgOut


def findMarker(
        img: List[List[int]], markerSize: int=4, 
        totalMarkers: int=250, draw: bool=True
        ) -> List[int]:
    """Finds Aruco marker, given an image."""

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParameters = aruco.DetectorParameters_create()
    bb, ids, rejected = aruco.detectMarkers(
            img, arucoDict, parameters=arucoParameters
            )

    if draw:
        aruco.drawDetectedMarkers(img, bb)
    return [bb, ids]


def replace(
        bb: int, ids: int,
        img: List[List[int]], imgR: List[List[int]], drawId: bool=True
        ) -> List[List[int]]:
    """Applies perspective transformation and replaces onto Aruco."""
    
    COLOR_BLACK = 0, 0, 0

    # Find corners in Aruco and given image.
    ul = bb[0][0][0], bb[0][0][1]
    ur = bb[0][1][0], bb[0][1][1]
    dr = bb[0][2][0], bb[0][2][1]
    dl = bb[0][3][0], bb[0][3][1]

    height, width = imgR.shape[:2]
    point1 = np.array([ul, ur, dr, dl])
    point2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])

    # Apply transformation to image.
    mtx, _ = cv2.findHomography(point2, point1)
    imgOutput = cv2.warpPerspective(imgR, mtx, (img.shape[1], img.shape[0]))

    # Add images together.
    cv2.fillConvexPoly(img, point1.astype(int), COLOR_BLACK)
    imgOutput += img
    return imgOutput