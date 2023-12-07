import cv2 
import pickle
import numpy as np

cap = cv2.VideoCapture("video.mp4")

def check(frame1):
    space_counter=0
    for pos in list:
        x,y = pos

        crop=frame1[y:y+15,x:x+26]
        count=cv2.countNonZero(crop)
        
        if count <= 150:
            color=(0,255,0)
        else:
            color=(0,0,255)

        cv2.rectangle(frame,pos,(pos[0]+26,pos[1]+15),color,2)
    

with open("noktalar1","rb") as f:
    list = pickle.load(f)

while True:
    _,frame = cap.read()
    
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(3,3),1)
    thresh=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    median=cv2.medianBlur(thresh,5)
    dilates=cv2.dilate(median,np.ones((3,3)),iterations=1)

    cv2.imshow("video",frame)
    check(dilates)

    if cv2.waitKey(200) & 0XFF == ord("q"):
        break

cap.release()

cv2.destroyAllWindows()