import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

# Loop until you hit the Esc key
while True:
    success, img = cap.read()
    imgBG = cv2.imread('imgBG.png')
    imgScaled = cv2.resize(img, (0, 0), None, 0.495, 0.635)

    cv2.imshow("Image", img)
    cv2.imshow("BG", imgBG)
    cv2.imshow("Scaled", imgScaled)


# Detect if the Esc key has been pressed
    c = cv2.waitKey(1)
    if c == 27:
        break

# Find Hands
    hands, img = detector.findHands(img)  # with draw

    if hands:
        hand = hands[0]
