import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import saveStatsModule as stats

fps = 0
sTime = time.time()
cTime = time.time()
counter = 0

cap = cv2.VideoCapture(0)

detector = htm.handDetector()

while True:

	counter += 1

	success, img = cap.read()

	detector.findHands(img)

	lmList = detector.findPosition(img)

	#if lmList:
	#	print(lmList[5])

	if time.time() - cTime > 1:
		fps = counter/(time.time()-cTime)
		counter = 0
		cTime=time.time()

	cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

	cv2.imshow("Image", img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

	if int(time.time() - sTime) % 20 == 0:
		stats.saveStats(__file__, int(fps))
