import cv2
import pickle
import cvzone
import numpy as np

# Video feed
cap = cv2.VideoCapture('D:\Python\Projects\Tinkerbetter\carPark.mp4')

with open('D:\Python\Projects\Tinkerbetter\CarParkPos', 'rb') as f:
    posList = pickle.load(f)

#width, height = 107, 48
total=len(posList)

#Lno=[0]*total
#print(posList)
#print(Lno)
d={}
ct=1
for i in posList:
    d[i]=ct
    ct+=1
print(d)

def checkParkingSpace(imgPro):
    spaceCounter = 0
    available=[]

    for pos in posList:
        x, y, w, h = pos

        imgCrop = imgPro[y:y + h, x:x + w]
        # cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop)

        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
            available.append(d[pos])
        else:
            color = (0, 0, 255)
            thickness = 2
        
        cv2.rectangle(img, (x, y), (x + w, y + h), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + h - 3), scale=1,thickness=2, offset=0, colorR=color)
        textct=str(d[pos])
        cvzone.putTextRect(img, textct, (x,y+12),scale=1,thickness=1, offset=0, colorR=(255,0,0))
        #cv2.putText(img, textct, (x,y+12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)
    
    cvzone.putTextRect(img, f'Available parking spaces: {spaceCounter}/{total}', (100, 40), scale=2,
                           thickness=4, offset=15, colorR=(0,200,0))
    textno=', '.join([str(i) for i in available])
    #cvzone.putTextRect(img, f'Slot numbers: {textno}', (100, 70), scale=1,thickness=2, offset=15, colorR=(0,200,0))

    (wt, ht), _ = cv2.getTextSize(textno, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
    x1=100
    y1=70   
    cv2.rectangle(img, (x1, y1 - 20), (x1 + wt, y1), (0,255,0), -1)
    cv2.putText(img, textno, (x1, y1 - 5),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 1)

while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)
    cv2.imshow("Image", img)
    # cv2.imshow("ImageBlur", imgBlur)
    # cv2.imshow("ImageThres", imgMedian)
    key=cv2.waitKey(1)
    if key == 27:  # Break the loop when 'Esc' key is pressed
        break
