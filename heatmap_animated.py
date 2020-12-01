import numpy as np
import time
import cv2

#LABELS = ["perfume", "tissue paper box", "playing cards", "book", "slippers", "pen", "butterfly knife", "paint brush", "toy car"]

#LABELS = ["pen", "tissue paper box", "toy car", "book", "perfume", "paint brush", "playing cards", "butterfly knife", "slippers"]
#LABELS = ["perfume", "pen", "playing cards", "book", "paint brush", "tissue paper box", "butterfly knife]", "toy car", "slippers"]

#LABELS = ["lotion", "glasses", "polish" ,"wallet"]
LABELS = ["car", "motorcycle", "people"]

np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

weightsPath = "mask-yolov3_10000.weights"
configPath = "mask-yolov3.cfg"

print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
vs = cv2.VideoCapture("output3.avi")

#getting top view images
top = cv2.imread('top.jpeg')/255
#cv2.imshow('Top',top)

#gaussian functionq
k=21
gauss=cv2.getGaussianKernel(k,np.sqrt(64))
gauss=gauss*gauss.T
gauss=(gauss/gauss[int(k/2),int(k/2)])
#cv2.imshow('Gauss',gauss)
print(top.shape[0])
print(top.shape[1])
j=cv2.applyColorMap(((1-gauss)*255).astype(np.uint8),cv2.COLORMAP_AUTUMN)/255.00
#  for
#vs = cv2.VideoCapture("http://192.168.18.14:8080/video")

# prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \ else cv2.CAP_PROP_FRAME_COUNT
# total = int(vs.get(prop))
heatmap=None
writer = None
(W, H) = (None, None)
points=[]
while True:
    print("hello")
    (grabbed, frame) = vs.read()
    if not grabbed:
        print("here?")
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
            if confidence > 0.4:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.3)

    if len(idxs) > 0:
        print("found box")
        for i in idxs.flatten():


            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            if len(points)<10:
                points.append([x,y])
            elif len(points)==10:
                points.pop(0)
                points.append([x, y])

    empty_image = np.zeros((top.shape[0], top.shape[1], 3)).astype(np.float32)

    for (x,y) in points:

        if x>top.shape[0]-11 or y>top.shape[1]-11 or x<11 or y<11:
            continue

        else:

            b = empty_image[x - int(k / 2):x + int(k / 2) + 1, y- int(k / 2):y + int(k / 2) + 1, :]

            print(x)
            print(y)
            print(b.shape)
            print(j.shape)
            c = j + b
            empty_image[x - int(k / 2):x + int(k / 2) + 1, y- int(k / 2):y + int(k / 2) + 1, :] = c

        g = cv2.cvtColor(empty_image, cv2.COLOR_BGR2GRAY)
        mask = np.where(g > 0.2, 1, 0).astype(np.float32)

        mask_3 = np.ones((top.shape[0], top.shape[1], 3)) * (1 - mask)[:, :, None]
        #cv2.imshow('reversemask', mask_3)
        mask_4 = empty_image * (mask)[:, :, None]

        # to remove the area where we need to put in the heat map
        new_top = mask_3 * top

        heatmap = new_top + mask_4
        cv2.imshow('heatmap', heatmap)

    else:
        print("no box found")

    if writer is None:
        #fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter("annotated_output.mp4v", cv2.VideoWriter_fourcc(*'mp4v'),10, (frame.shape[1], frame.shape[0]))
        #writer = cv2.VideoWriter("output_og_vid1.mp4", fourcc, 30, (frame.shape[1], frame.shape[0]), True)
        elap = (end - start)
        writ = cv2.VideoWriter("heatmap.mp4v", cv2.VideoWriter_fourcc(*'mp4v'),10, (top.shape[1], top.shape[0]))

        print("[INFO] single frame took {:.4f} seconds".format(elap))

    writer.write(frame)
    #writ.write(heatmap)
    frame=cv2.resize(frame,(1000,700),interpolation=cv2.INTER_CUBIC)
    cv2.imshow('image', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#     print("[INFO] cleaning up...")
writer.release()
vs.release()



