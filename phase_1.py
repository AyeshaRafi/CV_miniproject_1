import numpy as np
import cv2

# THREE INSTANCES OF THE LAPTOP WEBCAM ARE CREATED
# cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
# cap2 = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
# cap3 = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
# THREE VIDEOS ARE DISPLAYED IN THE CODE IN COMMENTS 
cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture("http://192.168.18.5:8081")
cap3 = cv2.VideoCapture("http://192.168.18.3:8080/video")
# checking if all caps are open
if cap.isOpened() and cap2.isOpened() and cap3.isOpened():
    while True:
        #reading a frame from the feeds
        ret, frame = cap.read()
        ret2, frame2 = cap2.read()
        ret3, frame3 = cap3.read()

        # if some video or feed returns an empty frame it is converted into a black screen
        if frame is None:
            frame = np.zeros((300, 400, 3), dtype=np.uint8)
        if frame2 is None:
            frame2 = np.zeros((300, 400, 3), dtype=np.uint8)
        if frame3 is None:
            frame3 = np.zeros((300, 400, 3), dtype=np.uint8)
        # frame is resized to fit better
        frame = cv2.resize(frame, (400, 300), interpolation=cv2.INTER_CUBIC)
        frame2 = cv2.resize(frame2, (400, 300), interpolation=cv2.INTER_CUBIC)
        frame3 = cv2.resize(frame3, (400, 300), interpolation=cv2.INTER_CUBIC)
        # frames are combined in a grid of four feeds
        frame_final = cv2.hconcat((frame, frame2))
        frame_final2 = cv2.hconcat((frame3, np.zeros((300, 400, 3), dtype=np.uint8)))
        final_frame = cv2.vconcat((frame_final, frame_final2))
        # show if there is something in the frame
        if final_frame is not None:
            cv2.imshow('frame', final_frame)
        # press q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
else:
    print("cap not opened")
cap.release()
cap2.release()
cap3.release()
cv2.destroyAllWindows()