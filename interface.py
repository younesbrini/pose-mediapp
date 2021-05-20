import cv2
import mediapipe as mp
import numpy as np
import os

from utils import calculate_angle
from position import load_asanas, Position, Asana
from clasifier import clasifier, maximum_error

#IMPORT THE ASANAS
dir_asana_path = os.getcwd()+'/src_asanas/'
asana_dict = load_asanas(dir_asana_path)

#MODEL
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)

## Setup mediapipe instance
with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5, model_complexity=1) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False


        ###### CLASIFIER SCRIPT
        try:

            #NORMAL LANDMARKS
            results = pose.process(image)
            landmarks = results.pose_landmarks.landmark
            h, w, _ = image.shape
            #FLIPPED LANDMARKS
            flip_image = cv2.flip(image, 1)
            flip_results = pose.process(flip_image)
            flip_landmarks = results.pose_landmarks.landmark
            #LANDMARKS PROCESSING
            position_test = Position(landmarks, w, h)
            position_test_flip = Position(flip_landmarks, w, h)
            #CLASSIFIER
            label, proba = clasifier(position_test, position_test_flip, asana_dict)
            # print("The position realized is {} at a {} % probability ".format(label, int(proba*100)))
            #CORRECTION 
            maxi_error, location = maximum_error(position_test.angles, asana_dict[label].angles)
            #print("The yogi should pay attention to his {} and correct it at {} degrees".format(location, int(maxi_error)))
            if position_test.angles[location] - asana_dict[label].angles[location] > 0 :
                correction = "close"
            else :
                correction = "open"
            #print("The yogi should {} his {} at {} degrees".format(correction, location, int(maxi_error)) )
        
            # Recolor back to BGR
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            #Location of writing
            writing_loc = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            cv2.putText(image, 'Position is = ' + label + ' at ' +str(int(proba*100)) +' % =>' + correction + ' your ' + location + ' at ' + str(int(maxi_error)) + ' degrees', 
                           tuple(np.multiply(writing_loc, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2, cv2.LINE_AA
                                )
                       
        except:
            pass
        
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()