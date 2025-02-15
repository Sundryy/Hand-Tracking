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

def test(result, width, height):
    if result.multi_hand_landmarks:
        
        for hand_landmarks in result.multi_hand_landmarks:
            index_tip = hand_landmarks.landmark[8]
            index_tip_pos = [index_tip.x * width, index_tip.y * height]

            thumb_tip = hand_landmarks.landmark[4]
            thumb_tip_pos = [thumb_tip.x * width, thumb_tip.y * height]

            
            
            #print('Y POSITION ',index_tip_pos[1],' ',  thumb_tip_pos[1])


            mp_drawing_utils.draw_landmarks(frame, hand_landmarks, hand.HAND_CONNECTIONS)

            print(index_tip_pos[0] - thumb_tip_pos[0])

        #circle_pos = (int(thumb_tip_pos[0] + index_tip_pos[0]) // 2, int(thumb_tip_pos[1]+ index_tip_pos[1] // 2))
        

        radius = 15
        colour = (255,0,0)
        thickness = 10
        #cv2.circle(frame, circle_pos, radius, colour, thickness)
        

    if index_tip_pos[0] - thumb_tip_pos[0] <= float(45) and thumb_tip_pos[1] - index_tip_pos[1] <= float(75):
        print('TOUCHING')
        #cv2.circle(frame, circle_pos, radius, colour, thickness)
    elif index_tip_pos[0] - thumb_tip_pos[0] > float(45) or thumb_tip_pos[1] - index_tip_pos[1] > float(75):
        print('NOT TOUCHING')

        #cv2.circle(frame, circle_pos, radius, colour, thickness)
    circle_pos = 0

    return index_tip_pos, thumb_tip_pos, circle_pos





while True:
    ret, frame = cam.read()
    #Detects hands within the image
    result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    #print(result.multi_hand_landmarks)


    if result.multi_hand_landmarks:    #If hands in camera essentially
        index_tip_pos, thumb_tip_pos, circle_pos = test(result,frame_width, frame_height)
        #print(index_tip_pos[1],'        ', thumb_tip_pos[1])
        '''
        height, width, _ = frame.shape

        circle_pos = (int(thumb_tip_pos[0] * width + thumb_tip_pos[0] * width) // 2, int(thumb_tip_pos[1] * height + index_tip_pos[1] * height // 2 ))

        
        radius = 15
        colour = (255,0,0)
        thickness = 10
        cv2.circle(frame, circle_pos, radius, colour, thickness)
        '''
        #print(circle_pos)

    # Display the captured frame
    frame = cv2.flip(frame, 1)
    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and writer objects
cam.release()

cv2.destroyAllWindows()
