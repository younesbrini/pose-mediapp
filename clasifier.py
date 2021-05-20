import os
import numpy as np

from position import Position, Asana, load_asanas
import get_landmarks

def distance(angles1, angles2):
    a1 = np.array(list(angles1.values()))
    a2 = np.array(list(angles2.values()))
    return np.linalg.norm(a1-a2)

def clasifier(position_test, position_test_flip, asana_dict):
    """
    Returns the most likely pose realized by the test position and the probability of the label
    """
    error_dict={}
    for name in asana_dict:
        error_dict[name] = min(distance(position_test.angles, asana_dict[name].angles), 
                                        distance(position_test_flip.angles, asana_dict[name].angles))
        #I only did this for conveniance. 
        # It is horribly wrong as we can determine beforehand if we should flip the image or not beforehand
    label = min(error_dict.keys(), key=(lambda k: error_dict[k]))

    #Probability measure that is super biased based on the asanas selected, but better than nothing
    clasifier_dict={}
    maxi = max(error_dict.values())
    for key in error_dict:
        clasifier_dict[key] = 1 - error_dict[key]/maxi 
    return (label, clasifier_dict[label])

def maximum_error(position_angles, asana_angles):
    maxi_error = 0
    location = ""
    for key in position_angles :
        if maxi_error < abs(position_angles[key] - asana_angles[key]):
            maxi_error = abs(position_angles[key] - asana_angles[key])
            location = key 
    return maxi_error, location

if __name__ == '__main__':
    #MODEL ASANAS
    dir_asana_path = os.getcwd()+'/src_asanas/'
    asana_dict = load_asanas(dir_asana_path)

    #TEST IMAGE
    image_test_path = os.getcwd()+'/test/downdog_test.jpg'
    landmarks, w, h = get_landmarks.extract_landmarks(image_test_path)
    flip_landmarks, w, h = get_landmarks.extract_landmarks(image_test_path, flip=True)
    position_test = Position(landmarks, w, h)
    position_test_flip = Position(flip_landmarks, w, h)

    #Clasify
    label, proba = clasifier(position_test, position_test_flip, asana_dict)
    print("The position realized is {} at a {} % probability ".format(label, int(proba*100)))

    #Error Max
    maxi_error, location = maximum_error(position_test.angles, asana_dict[label].angles)
    print("The yogi should pay attention to his {} and correct it at {} degrees".format(location, int(maxi_error)))
    if position_test.angles[location] - asana_dict[label].angles[location] > 0 :
        correction = "close"
    else :
        correction = "open"
    
    print("The yogi should {} his {} at {} degrees".format(correction, location, int(maxi_error)) )




    