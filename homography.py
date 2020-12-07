
import numpy as np
import cv2

file1 = open("h1.txt", 'r')
file2 = open("h2.txt", 'r')
file3 = open("h3.txt", 'r')


h1 = np.zeros((3, 3), dtype=np.float64)
for i in range(3):
    for j in range(3):
        h1[i][j] = file1.readline()

h2 = np.zeros((3, 3), dtype=np.float64)
for i in range(3):
    for j in range(3):
        h2[i][j] = file2.readline()

h3 = np.zeros((3, 3), dtype=np.float64)
for i in range(3):
    for j in range(3):
        h3[i][j] = file3.readline()


file1.close()
file2.close()
file3.close()

frame1_array=[]
frame2_array=[]
frame3_array=[]
combined_array=[]

cap1 = cv2.VideoCapture("videos/video1.avi")
cap2 = cv2.VideoCapture("videos/video2.avi")
cap3 = cv2.VideoCapture("videos/video3.avi")

out1 = cv2.VideoWriter('vid1.avi', cv2.VideoWriter_fourcc(*'mp4v'), 10, (1500, 1500))
out2 = cv2.VideoWriter('vid2.avi', cv2.VideoWriter_fourcc(*'mp4v'), 10, (1500, 1500))
out3 = cv2.VideoWriter('vid3.avi', cv2.VideoWriter_fourcc(*'mp4v'), 10, (1500, 1500))
out4 = cv2.VideoWriter('combined.avi', cv2.VideoWriter_fourcc(*'mp4v'), 10, (900, 700))

if cap1.isOpened() and cap2.isOpened() and cap3.isOpened():
    while True:
        # reading a frame from the feeds
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        ret3, frame3 = cap3.read()

        if frame1 is not None and frame2 is not None and frame3 is not None:
            frame1 = cv2.warpPerspective(frame1, h1, (1500, 1500))
            frame2 = cv2.warpPerspective(frame2, h2, (1500, 1500))
            frame3 = cv2.warpPerspective(frame3, h3, (1500, 1500))

            combined = cv2.addWeighted(frame1, 1, frame2, 1, 0)
            combined = cv2.addWeighted(combined, 1, frame3, 1, 0)[0:700, 0:900]

            out1.write(frame1)
            out2.write(frame2)
            out3.write(frame3)
            out4.write(combined)

            if combined is not None:
                cv2.imshow('frame', combined)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
else:
    check = 0
    print("cap not opened")


out1.release()
out2.release()
out3.release()
out4.release()

cap1.release()
cap2.release()
cap3.release()
cv2.destroyAllWindows()
