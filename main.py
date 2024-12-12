import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [AI, Player]
result_text = ""  # Define result_text with an initial value

good_deeds = [
    "Hold the door open for someone today.",
    "Help someone carry their groceries.",
    "Smile at a stranger.",
    "Donate to a charity.",
    "Compliment someone.",
    "Call a friend or family member to check in on them.",
    "Leave a positive review for a local business.",
    "Say 'thank you' to someone who deserves it."
]

while True:
    imgBG = cv2.imread("Resources/BG.png")
    success, img = cap.read()

    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    # Find Hands
    hands, img = detector.findHands(imgScaled)  # with draw

    if startGame:

        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 4:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3

                    randomNumber = random.randint(1, 3)
                    imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    # Player Wins
                    if (playerMove == 1 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1
                        result_text = "Victory is mine, and I will do the good deed to make up for your nothingness."

                    # AI Wins
                    if (playerMove == 3 and randomNumber == 1) or \
                            (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1
                        result_text = "Victory is mine! You? Redemption is a good deed. Go your penance awaits!"
                    cv2.putText(imgBG, result_text, (120, 140), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0), 2)
                    cv2.imshow("BG", imgBG)
                    cv2.waitKey(3000)  # Display the result for 3 seconds
                    cv2.destroyAllWindows()

    imgBG[234:654, 795:1195] = imgScaled

    if stateResult:
        cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
        cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

        # Display AI image if stateResult is True
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

        # Display a random good deed
        random_deed = random.choice(good_deeds)
        cv2.putText(imgBG, "Good Deed for the Day:", (450, 410), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.putText(imgBG, random_deed, (150, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        cv2.imshow("BG", imgBG)
        cv2.waitKey(120000)  # Display the good deed for 120 seconds

    cv2.imshow("BG", imgBG)

    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()