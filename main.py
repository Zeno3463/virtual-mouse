import cv2
import pyautogui
import time
from cvzone.HandTrackingModule import HandDetector

###### SETTINGS ######
moveSensitivity: int = 2 # the higher the number, the less sensitive the mouse will be
rectSize = 100

###### INITIALIZATION ######
video = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8)
pyautogui.FAILSAFE = False

###### FUNCTION DECLARATIONS ######
def calculateMousePositionBasedOnHandPosition(x, y):
	screenWidth, screenHeight = pyautogui.size()
	return int((x / rectSize) * screenWidth), int((y / rectSize) * screenHeight)

def calculateDistanceBtwTwoPoints(x1, y1, x2, y2):
	return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

###### MAIN LOOP ######
while True:
	success, img = video.read()
	img = cv2.flip(img, 1)
	hands, img = detector.findHands(img)
	# img = cv2.Canny(img, 600, 200)

	height, width, _ = img.shape

	img = cv2.rectangle(img, ((width//2)-rectSize, (height//2)-rectSize), ((width//2)+rectSize, (height//2)+rectSize), (0, 255, 0), 2)
	
	# if the hand is found
	if hands:
		lmList = hands[0]["lmList"]

		if (width//2)-rectSize <= lmList[8][0] <= (width//2)+rectSize and (height//2)-rectSize <= lmList[8][1] <= (height//2)+rectSize:
			# get the coordinates of the mouse
			x, y = calculateMousePositionBasedOnHandPosition(lmList[8][0], lmList[8][1])

			# # if the user's index finger is close to the user's middle finger (the user clicks)
			# if 10 < calculateDistanceBtwTwoPoints(lmList[8][0], lmList[8][1], lmList[4][0], lmList[4][1]) < 50:
			# 	# click the mouse
			# 	pyautogui.click(x, y)
			# 	# set a delay to prevent the user from clicking multiple times
			# 	time.sleep(0.5)
			# else:
			pyautogui.moveTo(x, y)

	cv2.imshow("Video", img)
	key = cv2.waitKey(1)
	if key == ord('q'):
		break