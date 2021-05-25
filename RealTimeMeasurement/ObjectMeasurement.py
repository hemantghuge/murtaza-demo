import cv2
import numpy as np
import utlis

##################

webcam = True
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

reqHeight = 500
imgContours2 = np.zeros((reqHeight, reqHeight, 3), np.uint8)

windowName = "Object Measurement"

cv2.namedWindow(windowName)

def emptyFunction(self):
	pass

# TrackBars
cv2.createTrackbar('cThreshold2_value', windowName, 0, 255, emptyFunction)

while True:

	#print('print')
	if webcam:
		success, img = cap.read()
	else:
		img = cv2.imread(path)

	img, conts = utlis.getContours(img, minArea=80000, filter=4, showCanny=True)

	if len(conts) != 0:
		biggest = conts[0][2]
		#print(biggest)
		imgWarp = utlis.warpImg(img, biggest, wP, hP)
		#cv2.imshow('A4 Paper', imgWarp)

		cThresh2_value = cv2.getTrackbarPos('cThreshold2_value', windowName)

		imgContours2, conts2 = utlis.getContours(imgWarp, minArea=200, filter=4, cThreshold=[cThresh2_value, cThresh2_value], showCanny=True)

		if len(conts2) != 0:
			for obj in conts2:
				cv2.polylines(imgContours2, [obj[2]], True, (0, 255, 0), 3)
				nPoints = utlis.reorder(obj[2])
				#print(nPoints)
				nW = round(utlis.findDist(nPoints[0][0]//scale, nPoints[1][0]//scale), 1)
				nH = round(utlis.findDist(nPoints[0][0]//scale, nPoints[2][0]//scale), 1)
				#print(nW, nH)

				cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[1][0][0], nPoints[1][0][1]), (255, 0, 255), 2)
				cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[2][0][0], nPoints[2][0][1]), (255, 0, 255), 2)

				x, y, w, h = obj[3]

				cv2.putText(imgContours2, '{}mm'.format(nW), (int(x+(w/2)), y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
				cv2.putText(imgContours2, '{}mm'.format(nH), (x, int(y+(h/2))), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)


		imgContours2 = utlis.rescaleImage(imgContours2, reqHeight=reqHeight)
		#cv2.imshow('A4 Paper', imgContours2)

	img = utlis.rescaleImage(img, reqHeight=reqHeight)

	final_image = utlis.concatenateImage(img, imgContours2)

	#img = cv2.resize(img, (0, 0), None, 0.5, 0.5)

	#cv2.imshow('Original', img)
	cv2.imshow(windowName, final_image)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
