import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)
timer=0
stateResult=False
startGame=False
# Loop until you hit the Esc key
while True:
    success, img = cap.read()
    imgBG = cv2.imread('imgBG.png')
    imgScaled = cv2.resize(img, (0, 0), None, 0.463, 0.685)
   
    # Find Hands
    hands, img = detector.findHands(imgScaled)  # with draw

    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (437, 325), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if hands:
                hand = hands[0]
                fingers= detector.fingersUp(hand)
                print(fingers)

    imgBG[157:486, 584:880] = imgScaled

    #cv2.imshow("Image", img)
    cv2.imshow("BG", imgBG)
    #cv2.imshow("Scaled", imgScaled)

    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame=True
        initialTime = time.time()
        stateResult = False


# Detect if the Esc key has been pressed
    c = cv2.waitKey(1)
    if c == 27:
        break


