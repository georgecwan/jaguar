import numpy as np
import cv2

# THIS FILE IS FOR TESTING PURPOSES ONLY
# DO NOT BOTHER RUNNING OR EDITING THIS FILE
# WILL LAG A LOT

faceCascade = cv2.CascadeClassifier('cv/Cascades/haarcascade_frontalface_default.xml')
profileCascade = cv2.CascadeClassifier('cv/Cascades/haarcascade_profileface.xml')
upperCascade = cv2.CascadeClassifier('cv/Cascades/haarcascade_upperbody.xml')
lowerCascade = cv2.CascadeClassifier('cv/Cascades/haarcascade_lowerbody.xml')
bodyCascade = cv2.CascadeClassifier('cv/Cascades/haarcascade_fullbody.xml')

RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
CYAN = (255, 255, 0)
MAGENTA = (255, 0, 255)
YELLOW = (0, 255, 255)

cap = cv2.VideoCapture(0)
# cap.set(3, 640) # set Width
# cap.set(4, 480) # set Height
while True:
    ret, img = cap.read()
    # img = cv2.flip(img, -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )
    profiles = profileCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )
    uppers = upperCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )
    lowers = lowerCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )
    bodies = bodyCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),BLUE,2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
    for (x,y,w,h) in profiles:
        cv2.rectangle(img,(x,y),(x+w,y+h),RED,2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
    for (x,y,w,h) in uppers:
        cv2.rectangle(img,(x,y),(x+w,y+h),GREEN,2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
    for (x,y,w,h) in lowers:
        cv2.rectangle(img,(x,y),(x+w,y+h),MAGENTA,2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
    for (x,y,w,h) in bodies:
        cv2.rectangle(img,(x,y),(x+w,y+h),YELLOW,2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
    cv2.imshow('bodyTest', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break
cap.release()
cv2.destroyAllWindows()
