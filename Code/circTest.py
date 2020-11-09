import numpy as np
import cv2 as cv

adr = 'D:\\Documents\\UNI\\CSCI318\\ART\\Imgs\\img_1.png'

#adr = 'C:\\Users\\Suker\\Pictures\\bottles.jpg'

image = cv.imread(adr)

output = image.copy()

gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

gray_blurred = cv.blur(gray,(3,3))

detected_circles = cv.HoughCircles(gray_blurred,cv.HOUGH_GRADIENT,1,20, param1=50,param2=30,minRadius=1,maxRadius=500)

if detected_circles is not None:
    detected_circles = np.uint16(np.around(detected_circles))

    for pt in detected_circles[0,:]:
        a,b,r = pt[0], pt[1], pt[2]

        cv.circle(output, (a,b), r, (0,0,255),2)
else:
    print("none found")
cv.imshow("circles",output)
cv.waitKey(0)

