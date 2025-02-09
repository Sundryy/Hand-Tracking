import cv2
import mediapipe as mp
import time
from pynput.keyboard import Key, Controller

#Initialises mediapipe hand detection
hand = mp.solutions.hands
#this allows hands to be detected and does all the landmarking
hands = hand.Hands()
#This allows connections between landmarks to be drawn
mp_drawing_utils = mp.solutions.drawing_utils


#THIS IS PYNPUT MODULE STUFF DELETE IF IT ISNT RIGHT
keyboard = Controller()




cam = cv2.VideoCapture(0)

frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:

    ret, frame = cam.read()
    #Detects hands within the image
    result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    #print(result.multi_hand_landmarks)

    if result.multi_hand_landmarks:    #If hands in camera essentially
        for hand_landmarks in result.multi_hand_landmarks:

            index_tip = hand_landmarks.landmark[8]
            index_tip_pos = [index_tip.x, index_tip.y]
            #index_tip_x = index_tip.x
            index_tip_y = index_tip.y

            index_base = hand_landmarks.landmark[5]
            index_base_pos = [index_base.x, index_base.y]
            #index_base_x = index_base.x
            index_base_y = index_base.y

            print(str(index_base_y) + 'this is BASE')
            print(index_tip_y)

            #THIS WORKS IT WILL MAKE IT STOP GOING RIGHT IF HOLDING A FIST OR IF POINTING UP AND DOWNWARDS
            if index_base_pos[0] - index_tip_pos[0] > 0.1:
                print('right')

            elif index_tip_pos[0] - index_base_pos[0] > 0.1:
                print('left')
            
            elif index_base_pos[1] - index_tip_pos[1] > 0.1:
                print('top')
                keyboard.press(Key.up)
            
            elif index_tip_pos[1] - index_base_pos[1] > 0.1:
                print('bottom')
                keyboard.press(Key.down)
                keyboard.release(Key.down)
            
                #FIND OUT WHICH KEY NEEDS TO BE RELEASED
            
            
            '''
            THIS WORKS IT CORRECTLY SHOWS THE DIRECTION I AM POINTING
            if index_base_pos[0] > index_tip_pos[0]:
                print('right')
            
            elif index_base_pos[0] < index_tip_pos [0]:
                print('left')
            '''
            mp_drawing_utils.draw_landmarks(frame, hand_landmarks, hand.HAND_CONNECTIONS)


    # Display the captured frame
    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and writer objects
cam.release()

cv2.destroyAllWindows()


