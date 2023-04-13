import cv2
import numpy as np


def initCrop(filename: str) -> None:
    """Initializes globals for cropping."""

    global img, imgCrop, ix, iy, ox, oy, cropping

    img = cv2.imread(filename)
    imgCrop = np.array([])
    ix, iy, ox, oy, = 0, 0, 0, 0
    cropping = False


def initDraw(filename: str) -> None:
    """Initializes globals for drawing."""

    global img, points

    img = cv2.imread(filename)
    points = []


def initMeasure() -> None:
    """Initializes globals for measuring."""

    global imgRect, imgRectCopy, imgRectMeas, ix, iy, drawing

    imgRect = np.array([])
    imgRectCopy = np.array([])
    imgRectMeas = np.array([])
    ix, iy = 0, 0
    drawing = False