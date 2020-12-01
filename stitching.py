import numpy as np
import cv2
import time
# THREE INSTANCES OF THE LAPTOP WEBCAM ARE CREATED
# THREE VIDEOS ARE DISPLAYED IN THE CODE IN COMMENTS
cap1 = cv2.VideoCapture("video1_top_view.avi")
cap2 = cv2.VideoCapture("video2_top_view.avi")
cap3 = cv2.VideoCapture("video3_top_view.avi")
#cap4 = cv2.VideoCapture("http://192.168.18.14:8080/video")
# checking if all caps are open
# testing to see github commits
frame1_array=[]
#frame2_array=[]
#frame3_array=[]
#frame4_array=[]
check=1
frame_no = 0
c_time = time.time()
if cap1.isOpened() and cap2.isOpened() and cap3.isOpened():
    while True:
        frame_no += 1
        # reading a frame from the feeds
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        ret3, frame3 = cap3.read()


        # if some video or feed returns an empty frame it is converted into a black screen
        if frame1 is None:
            frame1 = np.zeros((800, 600, 3), dtype=np.uint8)
        if frame2 is None:
            frame2 = np.zeros((800, 600, 3), dtype=np.uint8)
        if frame3 is None:
            frame3 = np.zeros((800, 600, 3), dtype=np.uint8)

        # frame is resized to fit better
        frame1 = cv2.resize(frame1, (800, 600), interpolation=cv2.INTER_CUBIC)
        frame2 = cv2.resize(frame2, (800, 600), interpolation=cv2.INTER_CUBIC)
        frame3 = cv2.resize(frame3, (800, 600), interpolation=cv2.INTER_CUBIC)

        frame1_abs = np.abs(frame1)
        frame2_abs = np.abs(frame2)
        frame3_abs = np.abs(frame3)

        combined = np.add(frame1_abs, frame2_abs)
        combined = np.add(combined, frame3_abs)
        combined = np.divide(combined, 10)
        frame1_array.append(combined)

        if combined is not None:
            cv2.imshow('frame', combined)
        # press q to quit

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
else:
    check=0
    print("cap not opened")


if check == 1:
    c_time2 = time.time()
    print("fps = ", frame_no / (c_time2 - c_time))
    out1 = cv2.VideoWriter('combined_video.mp4v', cv2.VideoWriter_fourcc(*'mp4v'), 10, (800, 600))
    #out2 = cv2.VideoWriter('video2.mp4v', cv2.VideoWriter_fourcc(*'mp4v'), 10, (400, 300))
    #out3 = cv2.VideoWriter('video3.mp4v', cv2.VideoWriter_fourcc(*'mp4v'), 10, (400, 300))
    #out4 = cv2.VideoWriter('video4.mp4v', cv2.VideoWriter_fourcc(*'mp4v'), 10, (400, 300))

    for i in range(len(frame1_array)):
        # writing to a image array
        out1.write(frame1_array[i])
    out1.release()


cap1.release()
cap2.release()
cap3.release()
cv2.destroyAllWindows()