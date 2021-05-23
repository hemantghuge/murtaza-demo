import cv2
import time
import mediapipe as mp
import saveStatsModule as stats

class handDetector():
	def __init__(self, mode=False, maxHands=2, detectionConf=0.5, trackConf=0.5):
		self.mode = mode
		self.maxHands = maxHands
		self.detectionConf = detectionConf
		self.trackConf = trackConf

		self.mpHands = mp.solutions.hands
		self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionConf, self.trackConf)
		self.mpDraw = mp.solutions.drawing_utils

	def findHands(self, img, draw=True):

		imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		self.results = self.hands.process(imgRGB)

		if self.results.multi_hand_landmarks:
			for handLms in self.results.multi_hand_landmarks:
				if draw:
					self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

		#return img

	def findPosition(self, img, handNo=0, draw=True):

		lmList = []

		if self.results.multi_hand_landmarks:
			myHand = self.results.multi_hand_landmarks[handNo]
			for id, lm in enumerate(myHand.landmark):
				h, w, c = img.shape
				#print(type(lm))
				cx, cy = int(lm.x * w), int(lm.y *h)
				lmList.append([id, cx, cy])
				cv2.circle(img, (cx, cy), 7, (255, 255, 255), cv2.FILLED)

		return lmList


def main():

	fps = 0
	sTime = time.time()
	cTime = time.time()
	counter = 0

	cap = cv2.VideoCapture(0)

	detector = handDetector()

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
			cTime = time.time()

		cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

		cv2.imshow("Image", img)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

		if int(time.time() - sTime) % 20 == 0:
			stats.saveStats(__file__, int(fps))

if __name__ == "__main__":
	main()
