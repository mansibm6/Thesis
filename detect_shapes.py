from detectorclass.ShapeDetector import ShapeDetector
import argparse
import imutils
import cv2
import numpy as np

#construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())

#load the image and resize it to a smaller factor so that the shapes can be approximated better
image = cv2.imread(args["image"])
resized = imutils.resize(image, width=300) #imutils is a custom package based on opencv by Adrian of pyimagesearch
ratio = image.shape[0] / float(resized.shape[0]) #we keep track of the ratio of the old height to the new resized height

#convert white backgroud to black
b_low = np.array([250,250,250])
b_up = np.array([255,255,255])
mask = cv2.inRange(resized, b_low, b_up)
resized[mask>0] = (0,0,0)

#convert the resized image to grayscale, blur it slightly, and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY) #converts image to grayscale
blurred = cv2.GaussianBlur(gray, (5, 5), 0) #reduces high frequency noise by slightly blurring the image
thresh = cv2.threshold(blurred, 10, 255, cv2.THRESH_BINARY)[1] #thresholding it to reveal the shapes

#find contours in the thresholded image and initialize the shape detector
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
sd = ShapeDetector()

#loop over the contours
for c in cnts:
	#compute the center of the contour, then detect the name of the
	#shape using only the contour
	M = cv2.moments(c)
	cX = int((M["m10"] / M["m00"]) * ratio)
	cY = int((M["m01"] / M["m00"]) * ratio)
	shape = sd.detect(c)
	#multiply the contour (x, y)-coordinates by the resize ratio,
	#then draw the contours and the name of the shape on the image
	c = c.astype("float") #converts to float
	c *= ratio
	c = c.astype("int")
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
		2, (5, 1, 74), 2)
	#show the output image
	cv2.imshow("Image", image)
	cv2.waitKey(0)
