import cv2
import numpy as np

overlay = []
overlay2 = []


def mark_point(event, x, y, params, something):
    if event == cv2.EVENT_LBUTTONDOWN:
        frame[y][x] = [0, 0, 255]
        overlay.append((x, y))


def mark_point2(event, x, y, params, something):
    if event == cv2.EVENT_LBUTTONDOWN:
        top_frame[y][x] = [0, 0, 255]
        overlay2.append((x, y))


cv2.namedWindow('image')
cv2.setMouseCallback('image', mark_point)
frame = cv2.imread("images3/image_47.jpg")
top_frame = cv2.imread("top_view24.jpeg")
while True:
    # ret, frame = cap.read()
    cv2.imshow('image', frame)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
    elif k == ord('a'):
        print(overlay)

cv2.namedWindow('image2')
cv2.setMouseCallback('image2', mark_point2)
while True:
    # ret, frame = cap.read()
    cv2.imshow('image2', top_frame)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
    elif k == ord('a'):
        print(overlay)

h = cv2.findHomography(np.array(overlay), np.array(overlay2))[0]
new_image = cv2.warpPerspective(frame, h, (1000, 1000))
cv2.destroyAllWindows()
while True:
    # ret, frame = cap.read()
    cv2.imshow('image2', new_image)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
# cv2.destroyAllWindows()
