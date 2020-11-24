
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

cap = cv2.VideoCapture("video1.mp4v")
cap1 = cv2.VideoCapture("video2.mp4v")
cap2 = cv2.VideoCapture("video3.mp4v")

images = []
i = 0
if cap.isOpened():
    while True:
        ret, frame = cap.read()
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if frame is not None and frame1 is not None and frame2 is not None:
            images.append(frame)
            images.append(frame1)
            images.append(frame2)
            stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
            (status, stitched) = stitcher.stitch(images)

            if status == 0:
                out1 = cv2.VideoWriter('video4.mp4v', cv2.VideoWriter_fourcc(*'mp4v'), 7, (1000, 800))
                out1.write(stitched)
            else:
                print("image stitching failed")
        else:
            break
        i += 1
        images.clear()
cap.release()
cv2.destroyAllWindows()