import numpy as np
import cv2

class Vision:
    def __init__(self):
        self.faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
        self.cap = cv2.VideoCapture(0)

    def get_bounding_box(self):
        ret, img = self.cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(20,20)
        )

        # Return the bounding box of the largest detected face
        max_area, mx, my, mw, mh = 0
        for (x, y, w, h) in faces:
            if w * h > max_area:
                max_area = w * h
                (mx, my, mw, mh) = (x, y, w, h)

        return (mx, my, mw, mh)


# Testing code
if __name__ == "__main__":
    faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
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
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
        cv2.imshow('Detect Face', img)
        k = cv2.waitKey(30) & 0xff
        if k == 27: # press 'ESC' to quit
            break
    cap.release()
    cv2.destroyAllWindows()
