# OTERO, Juan Cruz - 71459
# TP07 - Transformacion afin (incrustando imagenes)


import cv2
import numpy as np
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from vclib import globals as g
from vclib.callbacks import draw
from vclib.functions import affine


def main() -> None:
    COLOR_BLACK = 0, 0, 0
    PATH = 'fotos/hoja.png'
    PATH_FP = 'fotos/walrus.jpg'
    WINDOW = 'affine transformation'
    
    # Read image and footprint.
    g.initDraw(PATH)
    footprint = cv2.imread(PATH_FP)
    height, width = g.img.shape[:2]
    heightFp, widthFp = footprint.shape[:2]
    imgOut = np.zeros((height, width), np.uint8)
    
    while True:
        # Display image.
        cv2.imshow(WINDOW, g.img)
        
        # Wait for user instructions.
        k = cv2.waitKey(1) & 0xFF
        
        if k == ord('a'):
            # Ask for three points as input.
            cv2.namedWindow(WINDOW)
            cv2.setMouseCallback(WINDOW, draw)
        if len(g.points) == 3: 
            # Apply affine transformation to footprint.
            src = np.float32([[0, 0], [widthFp-1, 0], [0, heightFp-1]])
            des = np.float32([g.points])
            footprint = affine(footprint, src, des)[0:height, 0:width]
            
            # Create mask to position footprint.
            x, y = [x for x, _ in g.points], [y for _, y in g.points]
            mask = np.array(
                [[x[0], y[0]], 
                [x[2], y[2]], 
                [x[2]+x[1]-x[0], y[2]+y[1]-y[0]], 
                [x[1], y[1]]], np.int32
            )
            cv2.fillPoly(g.img, [mask], COLOR_BLACK, cv2.LINE_AA)
            
            # Add images together and save.
            imgOut = cv2.add(g.img, footprint)
            cv2.imwrite('fotos/output.png', imgOut)
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