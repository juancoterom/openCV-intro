# OTERO, Juan Cruz - 71459
# TP09 - Medicion de objetos


import cv2
import numpy as np
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from vclib import globals as g
from vclib.callbacks import measure
from vclib.functions import rectify


def main() -> None:
    PATH = 'fotos/foto.jpg'
    WINDOW = 'measurement on perspective-transformed image'

    # Read image. 
    g.initMeasure()
    img = cv2.imread(PATH)

    # Define size and vertices of image to transform.
    height, width = 360, 240 
    x1, y1 = 34, 205
    x2, y2 = 168, 215
    x3, y3 = 42, 403
    x4, y4 = 171, 381

    # Apply perspective transformation and save image.
    src = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
    des = np.float32(
        [[x1, y1], 
        [x1+width, y1],
        [x1, y1+height], 
        [x1+width, y1+height]]
    )
    g.imgRect = rectify(img, src, des)
    cv2.imwrite('fotos/foto_rect.jpg', g.imgRect)
    
    g.imgRectCopy = g.imgRect.copy()
    g.imgRectMeas = g.imgRect.copy()

    # Allow measurements on transformed image.
    cv2.namedWindow(WINDOW)
    cv2.setMouseCallback(WINDOW, measure)

    while True:
        # Display image.
        cv2.imshow(WINDOW, g.imgRect)

        # Wait for user instructions.
        k = cv2.waitKey(1) & 0xFF
        
        if k == ord('r'):
            # Reset measurements.
            g.imgRect = g.imgRectCopy.copy()
            g.imgRectMeas = g.imgRect.copy()
        if k == ord('q'):
            # Exit program.
            break

    # Save image with measurements and close windows.
    cv2.imwrite('fotos/foto_mediciones.jpg', g.imgRect)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()