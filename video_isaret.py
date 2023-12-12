import cv2 
import pickle
import numpy as np

cap = cv2.VideoCapture("video.mp4")

def check(frame1):
    space_counter=0
    for pos in liste:
        x,y = pos

        crop=frame1[y:y+15,x:x+26]
        count=cv2.countNonZero(crop)
        #print("count")
        
        if count <= 150:
            color=(0,255,0)
            space_counter+=1
        else:
            color=(0,0,255)

        cv2.rectangle(frame,pos,(pos[0]+24,pos[1]+12),color,2)
    
    percentage = int(100-(space_counter / len(liste)) * 100)

    cv2.putText(frame,f"doluluk:%{percentage}",(12,24),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),3)
    

with open("noktalar","rb") as f:
    liste = pickle.load(f)

while True:
    _,frame = cap.read()
    
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(3,3),1)
    thresh=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    median=cv2.medianBlur(thresh,5)
    dilates=cv2.dilate(median,np.ones((3,3)),iterations=1)


    check(dilates)
    cv2.imshow("video",frame)
    

    if cv2.waitKey(300) & 0XFF == ord("q"):
        break

cap.release()

cv2.destroyAllWindows()