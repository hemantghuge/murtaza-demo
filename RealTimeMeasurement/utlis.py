import cv2
import numpy as np

def getContours(img, cThreshold=[100, 100], showCanny=False, minArea=1000, filter=0, draw=False):
	imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
	imgCanny = cv2.Canny(imgBlur, cThreshold[0], cThreshold[1])

	kernel = np.ones((5, 5))
	imgDial = cv2.dilate(imgCanny, kernel, iterations=3)
	imgThresh = cv2.erode(imgDial, kernel, iterations=2)

	if showCanny:
		cv2.imshow('Canny', imgThresh)

	contours, hierarchy = cv2.findContours(imgThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	finalContours = []
	for i in contours:
		area = cv2.contourArea(i)

		if area > minArea:
			peri = cv2.arcLength(i, True)
			approx = cv2.approxPolyDP(i, 0.02*peri, True)
			bbox = cv2.boundingRect(approx)

			#print('check')
			#print(approx)
			#print(bbox)

			if filter > 0:
				if len(approx) == filter:
					finalContours.append([len(approx), area, approx, bbox, i])
			else:
				finalContours.append([len(approx), area, approx, bbox, i])


	finalContours = sorted(finalContours, key=lambda x:x[1], reverse=True)

	if draw:
		for con in finalContours:
			cv2.drawContours(img, con[4], -1, (0, 0, 255), 3)

	return img, finalContours

def reorder(myPoints):
	#print(myPoints)
	myPointsNew = np.zeros_like(myPoints)
	myPoints = myPoints.reshape((4, 2))

	add = myPoints.sum(1)
	#print(add)

	myPointsNew[0] = myPoints[np.argmin(add)]
	myPointsNew[3] = myPoints[np.argmax(add)]

	diff = np.diff(myPoints, axis=1)
	#print(diff)

	myPointsNew[1] = myPoints[np.argmin(diff)]
	myPointsNew[2] = myPoints[np.argmax(diff)]

	return myPointsNew

def warpImg(img, points, w, h, pad=5):
	#print(points)
	points = reorder(points)

	pts1 = np.float32(points)
	pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
	matrix = cv2.getPerspectiveTransform(pts1, pts2)
	imgWarp = cv2.warpPerspective(img, matrix, (w, h))
	imgWarp = imgWarp[pad:imgWarp.shape[0]-pad, pad:imgWarp.shape[1]-pad]

	return imgWarp

def findDist(pts1, pts2):
	return ((pts2[0] - pts1[0])**2 + (pts2[1] - pts1[1])**2 )**0.5

def rescaleImage(img, reqHeight=500):
	#print(img.shape[0], img.shape[1])
	reqWidth = int(reqHeight/img.shape[0]*img.shape[1])

	#print(reqHeight, reqWidth)
	resizedImg = cv2.resize(img, (reqWidth, reqHeight), interpolation=cv2.INTER_AREA)

	return resizedImg

def concatenateImage(img1, img2):

	if img1.shape[0] == img2.shape[0]:
		nH = img1.shape[0]
		nW = img1.shape[1]+img2.shape[1]

		blank_image = np.zeros((nH, nW, 3), np.uint8)

		blank_image[:, 0:img1.shape[1]] = img1
		blank_image[:, img1.shape[1]:] = img2

		#cv2.imshow('concatImage', blank_image)

		return blank_image
