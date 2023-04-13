# OTERO, Juan Cruz - 71459
# TP06 - Transformacion de similaridad


import cv2
import numpy as np
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from vclib import globals as g
from vclib.callbacks import crop
from vclib.functions import similarity


def main() -> None:
    COLOR_RED = 0, 0, 255
    PATH = 'fotos/hoja.png'
    WINDOW = 'image'

    # Read image.
    g.initCrop(PATH)

    # Allow cropping.
    cv2.namedWindow(WINDOW)
    cv2.setMouseCallback(WINDOW, crop)
    
    while True:
        imgCopy = g.img.copy()
        
        if not g.cropping:
            # Display original image.
            cv2.imshow(WINDOW, g.img)
        else:
            # Draw rectangle while cropping.
            cv2.rectangle(imgCopy, (g.ix, g.iy), (g.ox, g.oy), COLOR_RED, 2)
            cv2.imshow(WINDOW, imgCopy)

        # Wait for user instructions.
        k = cv2.waitKey(1) & 0xFF

        if k == ord('r'):
            # Restore original image.
            cv2.destroyWindow('cropped')
        if k == ord('s'):
            # Ask for transformation parameters. 
            valid_tx, valid_ty, valid_angle, valid_scale = (
                    False, False, False, False
                    )

            while not valid_tx:
                try:
                    tx = int(input('Tx: '))
                    valid_tx = True
                except ValueError:
                    print('ERROR: Ingresar entero.')
            while not valid_ty:
                try:
                    ty = int(input('Ty: '))
                    valid_ty = True
                except ValueError:
                    print('ERROR: Ingresar entero.')
            while not valid_angle:
                try:
                    angle = int(input('Angle: '))
                    valid_angle = True
                except ValueError:
                    print('Error: Ingresar entero.')
            while not valid_scale:
                try:
                    scale = float(input('Scale: '))
                    valid_scale = True
                except ValueError:
                    print('ERROR: Ingresar flotante.')

            # Apply similarity transformation and save image.
            imgSim = similarity(g.imgCrop, angle, tx, ty, scale)
            cv2.imwrite('fotos/similarity.png', imgSim)
            print('Imagen guardada.')
            cv2.destroyWindow('cropped')
        if k == ord('q'):
            # Exit program.
            break

    # Close windows.
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()