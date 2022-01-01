import cv2
import pyautogui
import time
from cvzone.HandTrackingModule import HandDetector

###### SETTINGS ######
rectSize = 200
xOffset = 100
yOffset = 170

###### INITIALIZATION ######
video = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.1)
pyautogui.FAILSAFE = False

###### FUNCTION DECLARATIONS ######
def calculateMousePositionBasedOnHandPosition(x, y, l, t):
	screenWidth, screenHeight = pyautogui.size()
	newX = x - l
	newY = y - t
	print(newX, newY)
	return int((newX / rectSize) * screenWidth), int((newY / rectSize) * screenHeight)

def calculateDistanceBtwTwoPoints(x1, y1, x2, y2):
	return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def drawRect(img, w, h):
	newImg = cv2.rectangle(img, ((w//2)-rectSize+xOffset, (h//2)-rectSize+yOffset), ((w//2)+xOffset, (h//2)+yOffset), (0, 255, 0), 2)
	return newImg, (w//2) - rectSize + xOffset, (h//2) - rectSize + yOffset, (w//2) + rectSize + xOffset, (h//2) + rectSize + yOffset

###### MAIN LOOP ######
while True:
	success, img = video.read()
	img = cv2.flip(img, 1)
	hands, img = detector.findHands(img)

	height, width, _ = img.shape

	img, left, top, right, bottom = drawRect(img, width, height)

	# if the hand is found
	if hands:
		lmList = hands[0]["lmList"]

		if left <= lmList[8][0] <= right and top <= lmList[8][1] <= bottom:
			# get the coordinates of the mouse
			x, y = calculateMousePositionBasedOnHandPosition(lmList[8][0], lmList[8][1], left, top)

			# if the user's index finger is close to the user's middle finger (the user clicks)
			if 10 < calculateDistanceBtwTwoPoints(lmList[8][0], lmList[8][1], lmList[4][0], lmList[4][1]) < 50:
				# click the mouse
				pyautogui.click(x, y)
				# set a delay to prevent the user from clicking multiple times
				time.sleep(0.5)
			else:
				pyautogui.moveTo(x, y)

	cv2.imshow("Video", img)
	key = cv2.waitKey(1)
	if key == ord('q'):
		break