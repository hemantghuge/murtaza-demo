import cv2
import numpy as np
import utlis

##################

webcam = False
path = 'fig1.jpg'
if webcam:
	cap = cv2.VideoCapture(2)
	cap.set(10, 160)
	cap.set(3, 1920)
	cap.set(4, 1080)

# 1280x720x3 In-Built Webcam
# 1280x960x3 Logitech Webcam

scale = 3

wP = 297 * scale
hP = 211 * scale

while True:

	print('print')
	if webcam:
		success, img = cap.read()
	else:
		img = cv2.imread(path)

	img, conts = utlis.getContours(img, minArea=50000, filter=4)

	if len(conts) != 0:
		biggest = conts[0][2]
		#print(biggest)
		imgWarp = utlis.warpImg(img, biggest, wP, hP)
		cv2.imshow('A4 Paper', imgWarp)


	img = cv2.resize(img, (0, 0), None, 0.5, 0.5)

	cv2.imshow('Original', img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
