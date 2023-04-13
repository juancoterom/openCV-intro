# OTERO, Juan Cruz - 71459
# TP11 - Alineacion de imagenes usando SIFT


import cv2
import numpy as np


def main() -> None:
    COLOR_BLUE = 255, 0, 0
    COLOR_RED = 0, 0, 255
    MIN_MATCH_COUNT = 10 

    # Read images.
    img1 = cv2.imread('fotos/screen1.jpg')
    img2 = cv2.imread('fotos/screen2.jpg')
    
    img1Copy = img1.copy()
    img2Copy = img2.copy()

    # Initialize detector and descriptor.
    dscr = cv2.xfeatures2d.SIFT_create(100)

    # Find keypoints and detectors with SIFT.
    kp1, des1 = dscr.detectAndCompute(img1, None)
    kp2, des2 = dscr.detectAndCompute(img2, None)

    # Graph keypoints.
    cv2.drawKeypoints(img1, kp1, img1Copy, COLOR_RED)
    cv2.drawKeypoints(img2, kp2, img2Copy, COLOR_BLUE)

    # Concatenate vertically.
    imgConcatenate = np.concatenate((img1Copy, img2Copy), axis=0)
    cv2.imshow('key points', imgConcatenate)
    cv2.imwrite('fotos/keypoints.jpg', imgConcatenate)
    cv2.waitKey(0)

    # Establish matches.
    matcher = cv2.BFMatcher(cv2.NORM_L2)
    matches = matcher.knnMatch(des1, des2, k=2)

    good = []
    all = []

    # Save good matches using Lowe's ratio test.
    for m, n in matches:
        all.append(m)
        if m.distance < 0.7*n.distance:
            good.append(m)

    if len(good) > MIN_MATCH_COUNT:
        # Compute homography with RANSAC.
        scrPts = np.float32(
                [kp1[m.queryIdx].pt for m in good]
                ).reshape(-1, 1, 2)
        dstPts = np.float32(
                [kp2[m.trainIdx].pt for m in good]
                ).reshape(-1, 1, 2)
        H, mask = cv2.findHomography(dstPts, scrPts, cv2.RANSAC, 5.0)
        
    # Apply perspective transformation H to img2.
    wimg2 = cv2.warpPerspective(img2, H, img2.shape[:2][::-1])

    # Display and save pre-Lowe matches.
    imgMatches = cv2.drawMatches(img1, kp1, img2, kp2, all, None)
    cv2.imshow('pre-Lowe matches', imgMatches)
    cv2.imwrite('fotos/prelowe_matches.jpg', imgMatches)
    cv2.waitKey(0)

    # Display and save post-Lowe matches.
    imgMatches = cv2.drawMatches(img1, kp1, img2, kp2, good, None)
    cv2.imshow('post-Lowe matches', imgMatches)
    cv2.imwrite('fotos/postlowe_matches.jpg', imgMatches)
    cv2.waitKey(0)

    # Blend both images.
    alpha = 0.5
    blend = np.array(wimg2*alpha + img1*(1-alpha), dtype=np.uint8)
    cv2.imshow('output image', blend)
    cv2.imwrite('fotos/output.jpg', blend)
    cv2.waitKey(0)
    
    # Close windows.
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()