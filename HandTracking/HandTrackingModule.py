import cv2
import time
import mediapipe as mp


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

#				for id, lm in enumerate(handLms.landmark):

		return img


def main():

	fps = 0
	cTime = time.time()
	counter = 0

	cap = cv2.VideoCapture(0)

	detector = handDetector()

	while True:

		counter += 1

		success, img = cap.read()
		img = detector.findHands(img)

		if time.time() - cTime > 1:
			fps = counter/(time.time()-cTime)
			counter = 0
			cTime = time.time()

		cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

		cv2.imshow("Image", img)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break


if __name__ == "__main__":
	main()
