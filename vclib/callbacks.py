import cv2
import numpy as np

from . import globals as g


def crop(event: int, x: int, y: int, flags: int, param: None) -> None:
    """Crops and displays a rectangular area, given an image."""

    if event == cv2.EVENT_LBUTTONDOWN:
        g.ix, g.iy, g.ox, g.oy = x, y, x, y
        g.cropping = True
    if event == cv2.EVENT_MOUSEMOVE and g.cropping:
        g.ox, g.oy = x, y
    if event == cv2.EVENT_LBUTTONUP:
        g.ox, g.oy = x, y
        g.cropping = False
        g.imgCrop = g.img.copy()[g.iy:g.oy, g.ix:g.ox]
        cv2.imshow('cropped', g.imgCrop)


def draw(event: int, x: int, y: int, flags: int, param: None) -> None:
    """Allows the user to draw points on a given image."""
    
    COLOR_RED = 0, 0, 255
    
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(g.img, (x, y), 2, COLOR_RED, -1)
        g.points.append([x, y])


def measure(event: int, x: int, y: int, flags: int, param: None) -> None:
    """Allows user to measure the distance between two points."""

    COLOR_RED = 0, 0, 255
    COLOR_YELLOW = 0, 255, 255

    if event == cv2.EVENT_LBUTTONDOWN:
        # Start measuring after left click.
        g.ix, g.iy = x, y
        g.drawing = True
    if event == cv2.EVENT_MOUSEMOVE and g.drawing:
        # Draw line as the mouse moves.
        g.imgRect[:] = g.imgRectMeas[:]
        cv2.line(g.imgRect, (g.ix, g.iy), (x, y), COLOR_RED, 2)

        # Calculate length in cm.
        meas = np.sqrt((g.ix-x)**2 + (g.iy-y)**2)/2

        # Write text onto image.
        xy_text = int((g.ix+x)/2 + 10), int((g.iy+y)/2 - 10)
        cv2.putText(
                g.imgRect, f'{meas:.2f} cm', xy_text,
                cv2.FONT_HERSHEY_PLAIN, 1, COLOR_YELLOW, 1
                )
    if event == cv2.EVENT_LBUTTONUP:
        # Finish measurement.
        g.imgRectMeas[:] = g.imgRect[:]
        g.drawing = False