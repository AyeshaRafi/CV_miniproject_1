import numpy as np
import cv2
import time
# THREE INSTANCES OF THE LAPTOP WEBCAM ARE CREATED
# THREE VIDEOS ARE DISPLAYED IN THE CODE IN COMMENTS
cap1 = cv2.VideoCapture("http://192.168.18.9:8081")
cap2 = cv2.VideoCapture("http://192.168.18.70:8081")
cap3 = cv2.VideoCapture("http://192.168.18.3:8080/video")
cap4 = cv2.VideoCapture("http://192.168.18.5:8081")
# checking if all caps are open
frame1_array=[]
frame2_array=[]
frame3_array=[]
frame4_array=[]
check=1
frame_no = 0
c_time = time.time()
if cap1.isOpened() and cap2.isOpened() and cap3.isOpened() and cap4.isOpened():
    while True:
        frame_no += 1
        # reading a frame from the feeds
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        ret3, frame3 = cap3.read()
        ret4, frame4 = cap4.read()
        frame1_array.append(frame1)
        frame2_array.append(frame2)
        frame3_array.append(frame3)
        frame4_array.append(frame4)
        # if some video or feed returns an empty frame it is converted into a black screen
        if frame1 is None:
            frame1 = np.zeros((300, 400, 3), dtype=np.uint8)
        if frame2 is None:
            frame2 = np.zeros((300, 400, 3), dtype=np.uint8)
        if frame3 is None:
            frame3 = np.zeros((300, 400, 3), dtype=np.uint8)
        if frame4 is None:
            frame4 = np.zeros((300, 400, 3), dtype=np.uint8)
        # frame is resized to fit better
        frame1 = cv2.resize(frame1, (400, 300), interpolation=cv2.INTER_CUBIC)
        frame2 = cv2.resize(frame2, (400, 300), interpolation=cv2.INTER_CUBIC)
        frame3 = cv2.resize(frame3, (400, 300), interpolation=cv2.INTER_CUBIC)
        frame4 = cv2.resize(frame4, (400, 300), interpolation=cv2.INTER_CUBIC)
        frame1_array.append(frame1)
        frame2_array.append(frame2)
        frame3_array.append(frame3)
        frame4_array.append(frame4)

        # frames are combined in a grid of four feeds
        frame_final1 = cv2.hconcat((frame1, frame2))
        frame_final2 = cv2.hconcat((frame3, frame4))
        final_frame = cv2.vconcat((frame_final1, frame_final2))
        # show if there is something in the frame
        if final_frame is not None:
            cv2.imshow('frame', final_frame)
        # press q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
else:
    check=0
    print("cap not opened")


if check == 1:
    c_time2 = time.time()
    print("fps = ", frame_no / (c_time2 - c_time))
    out1 = cv2.VideoWriter('video1.mp4v', cv2.VideoWriter_fourcc(*'mp4v'), 10, (400, 300))
    out2 = cv2.VideoWriter('video2.mp4v', cv2.VideoWriter_fourcc(*'mp4v'), 10, (400, 300))
    out3 = cv2.VideoWriter('video3.mp4v', cv2.VideoWriter_fourcc(*'mp4v'), 10, (400, 300))
    out4 = cv2.VideoWriter('video4.mp4v', cv2.VideoWriter_fourcc(*'mp4v'), 10, (400, 300))

    for i in range(len(frame1_array)):
        # writing to a image array
        out1.write(frame1_array[i])
    out1.release()

    for i in range(len(frame2_array)):
        # writing to a image array
        out2.write(frame2_array[i])
    out2.release()

    for i in range(len(frame3_array)):
        # writing to a image array
        out3.write(frame3_array[i])
    out3.release()
    for i in range(len(frame4_array)):
        # writing to a image array
        out4.write(frame4_array[i])
    out4.release()

cap1.release()
cap2.release()
cap3.release()
cv2.destroyAllWindows()