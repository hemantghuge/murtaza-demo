import cv2
import numpy as np

##################

webcam = False
path = 'fig1.jpg'
cap = cv2.VideoCapture(2)
cap.set(10, 160)
cap.set(3, 1920)
cap.set(4, 1080)

# 1280x720x3 In-Built Webcam
# 1280x960x3 Logitech Webcam

while True:

	success, img = cap.read()

	print(img.shape)

	cv2.imwrite(path, img)

	cv2.imshow('Original', img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
