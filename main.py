# cvzone source code -> https://github.com/cvzone/cvzone/tree/master

import cv2 as cv
import cvzone
import random
from cvzone.HandTrackingModule import HandDetector
import time

video = cv.VideoCapture(0)
video.set(3,640)
video.set(4,480)
hand_detector = HandDetector(maxHands=1)
startGame = False
stateResult = False
winner = ''
abc = 123
while True:
    background = cv.imread('Resources/BG.png')
    rock = cv.imread('Resources/1.png')
    paper = cv.imread('Resources/2.png')
    scissors = cv.imread('Resources/3.png')

    frame,img = video.read()
    img = cv.flip(img,1)
    imagScaled = cv.resize(img, (0,0), None, 0.875, 0.875)
    
    imagScaled = imagScaled[:,80:480]

    find_hand, img = hand_detector.findHands(imagScaled,flipType=False)
    ai_score = 0
    player_score = 0
    # print(find_hand)
    # print(img)
    if startGame:
        #print("S is pressed", time.time())

        if stateResult is False:
            timer = time.time() - initialTimer
            cv.putText(background, str(int(timer)), (600,430), cv.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 2)

            if timer > 3:
                stateResult = True
                timer = 0

            # background = cvzone.overlayPNG(background, img_ai, (50,50))
            
                if find_hand:
                    player_move = None
                    fingers = hand_detector.fingersUp(find_hand[0])
                    #print(fingers)
                    if fingers == [1,0,0,0,0]:
                        player_move = 1 #rock
                    elif fingers == [0,1,1,1,1]:
                        player_move = 2 #paper
                    elif fingers == [1,1,1,0,0]:
                        player_move = 3 #scissors

                    ai_choice = random.randint(1,3)
                    img_ai = cv.imread(f'Resources/{ai_choice}.png', cv.IMREAD_UNCHANGED)
                    background = cvzone.overlayPNG(background,img_ai,(60,50))
                    if player_move == ai_choice:
                        winner = "Draw"
                    elif (player_move == 1 and ai_choice == 3) or (player_move == 2 and ai_choice == 1) or (player_move == 3 and ai_choice == 2):
                        winner = "Player"
                        player_score += 1
                    elif (player_move == 3 and ai_choice == 1) or (player_move == 1 and ai_choice == 2) or (player_move == 2 and ai_choice == 3):
                        winner = "AI"
                        ai_score += 1
                    print(winner)
                    

                    # check winner
    imagScaled_resize = cv.resize(imagScaled,(300,300))               
    background[300:600, 800:1100] = imagScaled_resize #300x300
    if stateResult:
        background = cvzone.overlayPNG(background,img_ai,(130,260))

    cv.imshow("Background", background)

    if cv.waitKey(1) == ord('s'):
        startGame = True
        initialTimer = time.time()
        stateResult = False
        
    

#scoreboard, display winner after 3 rounds