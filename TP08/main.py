# OTERO, Juan Cruz - 71459
# TP08 - Rectificando imagenes


import cv2
import numpy as np
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from vclib import globals as g
from vclib.callbacks import draw
from vclib.functions import rectify


def main() -> None:
    PATH = 'fotos/lemon.jpg'
    WINDOW = 'perspective transformation'
    
    # Read image.
    g.initDraw(PATH)
    height, width = 300, 600
    
    while True:
        # Display image.
        cv2.imshow(WINDOW, g.img)
        
        # Wait for user instructions.
        k = cv2.waitKey(1) & 0xFF
        
        if k == ord('h'):
            # Ask for four points as input.
            cv2.namedWindow(WINDOW)
            cv2.setMouseCallback(WINDOW, draw)
        if len(g.points) == 4:
            # Apply perspective transformation.
            src = np.float32([g.points])
            des = np.float32(
                    [[0, 0], 
                     [width-1, 0], 
                     [0, height-1], 
                     [width-1, height-1]]
                    )
            img_out = rectify(g.img, src, des)[0:height, 0:width]

            # Save image.
            cv2.imwrite('fotos/output.jpg', imgOut)
            break
        if k == ord('q'):
            # Exit program.
            break
    
    # Display output image and close windows.
    cv2.imshow('output image', imgOut)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()