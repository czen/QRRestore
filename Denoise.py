import cv2
import numpy

filein = "data/1.jpg"
fileout = "out1.jpg"
#read in grayscale:
img = cv2.imread(filein, cv2.IMREAD_GRAYSCALE)
#remove noise:
img = cv2.fastNlMeansDenoising(img, 12, 12, 7, 21)
#convert to binary b/w:
(thresh, img) = cv2.threshold(img, 290, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
thresh = 250 #85
img = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]
#morpho transformation:
kernel = numpy.ones((5, 5), numpy.uint8)
img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
img = cv2.dilate(img, kernel,iterations=1)
img = cv2.erode(img, kernel,iterations=1)
#resize the image to 116x116 px:
img = cv2.resize(img, (116, 116), interpolation=cv2.INTER_CUBIC)
#save the image:
cv2.imwrite(fileout, img)