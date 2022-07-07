import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import glob
import numpy as np


def get_AiChoice(random_image):
    # leave the last 4 letters (.png) and gives the rest
    ai_choice = random_image[:-4]
    if ai_choice == 'rock':
        return 1
    elif ai_choice == 'paper':
        return 2
    else:
        return 3


def getScore(playerMove, aiMove, scores):
    aiScore = scores[0]
    playerScore = scores[1]
    if (playerMove == aiMove):  # if player and ai make the same move
        return [aiScore, playerScore]
    if (playerMove == 1 and aiMove == 3) or (playerMove == 2 and aiMove == 1) or (playerMove == 3 and aiMove == 2):  # if player move wins
        return [aiScore, playerScore+1]
    # if ai move wins # (playerMove==3 and aiMove==1) or (playerMove==1 and aiMove==2) or (playerMove==2 and aiMove==3):
    else:
        return [aiScore+1, playerScore]


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [AI, Player]

while True:
    imgBG = cv2.imread("imgBG.png")
    success, img = cap.read()

    imgScaled = cv2.resize(img, (0, 0), None, 0.463, 0.685)

    # Find Hands
    hands, img = detector.findHands(imgScaled)  # with draw

    if startGame:

        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (437, 325),
                        cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    playerMoveStr = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                        playerMoveStr = 'rock'
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                        playerMoveStr = 'paper'
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3
                        playerMoveStr = 'scissor'

                    img_files = []
                    for file in glob.glob("*.png"):
                        img_files.append(file)

                    random_image = img_files[np.random.randint(1, 4)]

                    # calculating score
                    random_image = img_files[np.random.randint(1, 4)]
                    aiMove = get_AiChoice(random_image)
                    print("You chose: "+playerMoveStr + "  and AI Chose: " +
                          random_image[:-4]+"("+str(aiMove)+")")  # for self-check
                    scores = getScore(playerMove, aiMove, scores)
                    print(scores)

                    randimg = cv2.imread(random_image, cv2.IMREAD_UNCHANGED)

    imgBG[157:486, 584:880] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, randimg, (110, 250))
        # to display score in the background.
        scoreString = str(scores[0])+" - "+str(scores[1])
        cv2.putText(imgBG, str(scoreString), (395, 310),
                    cv2.FONT_HERSHEY_PLAIN, 3, (147, 123, 184), 4)

    cv2.imshow("BG", imgBG)

    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False

    c = cv2.waitKey(1)
    if c == 27:
        break
