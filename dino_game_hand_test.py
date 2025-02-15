import pynput
import cv2
import mediapipe as mp
import time
import keyboard

pressed = False



#Initialises mediapipe hand detection
hand = mp.solutions.hands
#this allows hands to be detected and does all the landmarking
hands = hand.Hands()
#This allows connections between landmarks to be drawn
mp_drawing_utils = mp.solutions.drawing_utils




cam = cv2.VideoCapture(0)

frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))


def test(result):
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            index_tip = hand_landmarks.landmark[8]
            index_tip_pos = [index_tip.x, index_tip.y]
            #index_tip_x = index_tip.x
            index_tip_y = index_tip.y

            index_base = hand_landmarks.landmark[5]
            index_base_pos = [index_base.x, index_base.y]
            #index_base_x = index_base.x
            index_base_y = index_base.y

            #print(str(index_base_y) + 'this is BASE')
            #print(index_tip_y)
            print(index_tip_pos[1] - index_base_pos[1])
            mp_drawing_utils.draw_landmarks(frame, hand_landmarks, hand.HAND_CONNECTIONS)

        return index_base_pos, index_tip_pos

def keyboardAction(index_base_pos, index_tip_pos):
    global pressed
    if index_base_pos[0] - index_tip_pos[0] > 0.1:
        keyboard.press('right')
        print('right')
        #pressed = False
        #release = 'right'

    elif index_tip_pos[0] - index_base_pos[0] > 0.1:
        keyboard.press('left')
        print('left')
        #pressed = False
        #release = 'left'
            
    elif index_base_pos[1] - index_tip_pos[1] > 0.1:
        print('top')
        keyboard.press('up')
       # pressed = False
        #release = 'up'
        
      
    elif index_tip_pos[1] - index_base_pos[1] > 0.25 :
        #if pressed == False:
        keyboard.press('down')
        print('down')
        #release = 'down'

    else:
        keyboard.release('up'), keyboard.release('down'), keyboard.release('left'), keyboard.release('right')
    



while True:
    ret, frame = cam.read()
    #Detects hands within the image
    result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    #print(result.multi_hand_landmarks)


    if result.multi_hand_landmarks:    #If hands in camera essentially
        index_base_pos, index_tip_pos = test(result)
        keyboardAction(index_base_pos,index_tip_pos)

    # Display the captured frame
    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and writer objects
cam.release()

cv2.destroyAllWindows()
