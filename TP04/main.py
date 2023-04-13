# OTERO, Juan Cruz - 71459
# TP04 - Manipulacion de imagenes


import cv2
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from vclib import globals as g
from vclib.callbacks import crop


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

        if k == ord('g'):
            # Save cropped image.
            cv2.imwrite('fotos/cropeado.png', g.imgCrop)
        if k == ord('r'):
            # Restore original image.
            cv2.destroyWindow('cropped')
        if k == ord('q'):
            # Exit program.
            break

    # Close windows.
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()