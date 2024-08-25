import cv2
import pickle

def nothing(x):
    pass

# width, height = 107, 48

try:
    with open('D:\Python\Projects\Tinkerbetter\CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

def mouseClick(events, x, y, flags, params):
    # Get the current values of the trackbars
    w = cv2.getTrackbarPos('Width', 'Image')
    h = cv2.getTrackbarPos('Height', 'Image')
    
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y, w, h))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1, w1, h1 = pos
            if x1 < x < x1 + w and y1 < y < y1 + h:
                posList.pop(i)

    with open('D:\Python\Projects\Tinkerbetter\CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

cv2.namedWindow('Image')
# Create trackbars outside the loop
cv2.createTrackbar('Width', 'Image', 107, 250, nothing)
cv2.createTrackbar('Height', 'Image', 48, 250, nothing)

while True:
    img = cv2.imread('carParkImg.png')
    
    for pos in posList:
        x, y, w, h = pos
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
    
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    key = cv2.waitKey(1)

    if key == 27:  # Break the loop when 'Esc' key is pressed
        break

cv2.destroyAllWindows()
