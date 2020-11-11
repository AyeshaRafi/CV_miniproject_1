import cv2
cap = cv2.VideoCapture("video4.mp4v")
i = 0
if cap.isOpened():
    while True:
        ret, frame = cap.read()
        if frame is not None:
            cv2.imwrite("images2/image_{0}.jpg".format(i), frame)
        else:
            break
        i += 1
cap.release()
cv2.destroyAllWindows()