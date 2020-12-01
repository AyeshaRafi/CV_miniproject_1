`import numpy as np
import cv2
import matplotlib.pyplot as plt
import time
# THREE INSTANCES OF THE LAPTOP WEBCAM ARE CREATED
# THREE VIDEOS ARE DISPLAYED IN THE CODE IN COMMENTS
#cap1 = cv2.VideoCapture("video1_top_view.avi")
#cap2 = cv2.VideoCapture("video2_top_view.avi")
#cap3 = cv2.VideoCapture("video3_top_view.avi")
#cap4 = cv2.VideoC  apture("http://192.168.18.14:8080/video")
# checking if all caps are open
# testing to see github commits
frame1_array=[]
#frame2_array=[]
#frame3_array=[]
#frame4_array=[]
check=1
frame_no = 0
c_time = time.time()


#getting top view images
top = cv2.imread('top.png')/255
cv2.imshow('Top',top)

#gaussian function
k=21
gauss=cv2.getGaussianKernel(k,np.sqrt(64))
gauss=gauss*gauss.T
gauss=(gauss/gauss[int(k/2),int(k/2)])
cv2.imshow('Gauss',gauss)

#array to keep all k points that we will be putting on the screen

points=[[10,20],[50,30],[100,150],[200,16]]

#making blank image to create a mask
empty_image = np.zeros((top.shape[0], top.shape[1], 3)).astype(np.float32)
j=cv2.applyColorMap(((1-gauss)*255).astype(np.uint8),cv2.COLORMAP_AUTUMN)/255.00
cv2.imshow('Gaussian',j)

for p in points:
    b=empty_image[ p[0]-int(k/2):p[0]+int(k/2)+1 , p[1]-int(k/2):p[1]+int(k/2)+1, : ]
    c=j+b
    empty_image[ p[0]-int(k/2):p[0]+int(k/2)+1 , p[1]-int(k/2):p[1]+int(k/2)+1, : ]=c

print(np.max(empty_image,axis=(0,1)))
n=np.max(empty_image,axis=(0,1))+0.0001
empty_image=empty_image/n
cv2.imshow('masked image',empty_image)

#making inverse mask

g=cv2.cvtColor(empty_image,cv2.COLOR_BGR2GRAY)
mask=np.where(g>0.2,1,0).astype(np.float32)

mask_3=np.ones((top.shape[0],top.shape[1],3))*(1-mask)[:,:,None]
cv2.imshow('reversemask',mask_3)

mask_4=empty_image*(mask)[:,:,None]

# to remove the area where we need to put in the heat map
new_top=mask_3*top

heatmap=new_top+mask_4


while True:
    cv2.imshow('heatmap', heatmap)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break`