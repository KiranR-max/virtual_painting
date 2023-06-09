import cv2
import numpy as np

x,y,k = 200,200,-1
cap = cv2.VideoCapture(0)

def set_input(event, x1, y1,flag,param):
    global x, y, k
    if event == cv2.EVENT_LBUTTONDOWN:
        x = x1
        y = y1
        k = 1

cv2.namedWindow("Set_point")
cv2.setMouseCallback("Set_point", set_input)

#taking input 
while True: 
    _, inp_img = cap.read()
    inp_img = cv2.flip(inp_img, 1)
    grayImg = cv2.cvtColor(inp_img, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow("_point", inp_img)
    if k == 1 or cv2.waitKey(30) == 27:
        cv2.destroyAllWindows()
        break

stp = 0

old_pts = np.array([[x, y]], dtype=np.float32).reshape(-1,1,2)
mask = np.zeros_like(inp_img)

while True:
    _, newImg = cap.read()
    newImg = cv2.flip(newImg, 1)
    new_gray = cv2.cvtColor(newImg, cv2.COLOR_BGR2GRAY)     
    new_pts,status,err = cv2.calcOpticalFlowPyrLK(grayImg, 
                         new_gray, 
                         old_pts, 
                         None, maxLevel=1,
                         criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                                                         15, 0.08))

    for i, j in zip(old_pts, new_pts):
        x,y = j.ravel()
        a,b = i.ravel()
        if cv2.waitKey(2) & 0xff == ord('p'):
            stp = 1
            
        elif cv2.waitKey(2) & 0xff == ord('b'):
            stp = 0
        
        elif cv2.waitKey(2) == ord('c'):
            mask = np.zeros_like(newImg)
            
        if stp == 0:
            mask = cv2.line(mask, (a,b), (x,y), (0,0,255), 6)

        cv2.circle(newImg, (x,y), 6, (0,255,0), -1)
    
    newImg = cv2.addWeighted(mask, 0.3, newImg, 0.7, 0)
    cv2.putText(mask, "'p':Pause 'b':Begin 'c':Clear", (10,50), 
                cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255))
    cv2.imshow("Ouput", newImg)
    cv2.imshow("Result", mask)

    
    grayImg = new_gray.copy()
    old_pts = new_pts.reshape(-1,1,2)
    
    if cv2.waitKey(1) & 0xff == 27:
        break

cap.release()
cv2.destroyAllWindows()