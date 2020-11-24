import numpy as np
import argparse
# import imutils
import time
import cv2
import os
LABELS = ["perfume", "tissue paper box", "playing cards", "book", "paint brush", "pen", "butterfly knife]", "toy car",
          "slippers"]
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

weightsPath = "mask-yolov3_10000.weights"
configPath = "mask-yolov3.cfg"

print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
vs = cv2.VideoCapture("video4.mp4v")
#  for 
#vs = cv2.VideoCapture("http://192.168.18.14:8080/video")
# prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \ else cv2.CAP_PROP_FRAME_COUNT
# total = int(vs.get(prop))
writer = None
(W, H) = (None, None)

while True:
    (grabbed, frame) = vs.read()
    if not grabbed:
        break
    if W is None or H is None:
        (H, W) = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    start = time.time()
    layerOutputs = net.forward(ln)
    end = time.time()
    boxes = []
    confidences = []
    classIDs = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            #             print(confidence)
            if confidence > 0.5:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)
    if len(idxs) > 0:
        print("found box")
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            color = [int(c) for c in COLORS[classIDs[i]]]
            cv2.rectangle(frame, (x,y), (x + w , y + h), color, 1)
            text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
            cv2.putText(frame, text, (x-20, y + h + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    if writer is None:
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter("output_og_vid1.mp4", fourcc, 30, (frame.shape[1], frame.shape[0]), True)
        elap = (end - start)
        print("[INFO] single frame took {:.4f} seconds".format(elap))
    frame=cv2.resize(frame,(1000,700),interpolation=cv2.INTER_CUBIC)
    writer.write(frame)
    cv2.imshow('image', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#     print("[INFO] cleaning up...")
writer.release()
vs.release()