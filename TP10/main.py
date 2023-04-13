# OTERO, Juan Cruz - 71459
# TP10 - Practico libre ArUCo


import cv2
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from vclib.functions import findMarker, replace


def main() -> None:
    PATH = 'fotos/messi.jpg'
    WINDOW = 'aruco'

    # Open camera and read image. 
    cap = cv2.VideoCapture(0)
    mask = cv2.imread(PATH)

    while True:
        # Read video and find Aruco.
        ret, img = cap.read()
        arucoFound = findMarker(img)

        if len(arucoFound[0]) != 0:
            # Replace image onto Aruco.
            for bb, id in zip(arucoFound[0], arucoFound[1]):
                img = replace(bb, id, img, mask)

        # Display modified image.
        cv2.imshow(WINDOW, img)

        # Wait for user input.
        k = cv2.waitKey(1) & 0xFF

        if k == ord('q'):
            # Exit program.
            break


if __name__ == '__main__':
    main()