# OTERO, Juan Cruz - 71459
# TP02 - Segmentando una imagen

import cv2
import numpy as np
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from vclib.functions import thresh


def main() -> None:
    PATH = 'fotos/hoja.png'

    # Read image.
    img = cv2.imread(PATH, cv2.IMREAD_GRAYSCALE)

    # Apply thresholding
    img_out = np.array(thresh(img))

    # Write image.
    cv2.imwrite('fotos/resultado.png', img_out)


if __name__ == '__main__':
    main()