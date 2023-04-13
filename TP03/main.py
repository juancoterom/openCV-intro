# OTERO, Juan Cruz - 71459
# TP03 - Propiedades de video

import cv2
import sys


def main() -> None:
    # Input video as argument.
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print('Pasar archivo como argumento.')
        sys.exit(0)

    cap = cv2.VideoCapture(filename)
    
    # Get codec, framesize, FPS and delay.
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    framesize = width, height
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = int(1000/fps)
    print(f'Framesize: {framesize}; FPS: {fps}; Delay: {delay} ms')

    # Output file.
    out = cv2.VideoWriter('videos/output.avi', fourcc, fps, framesize, False)

    # Play grayscale video.
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            out.write(gray)
            cv2.imshow('Grayscale Video', gray)
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break
        else:
            break
    
    # Close window.
    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()