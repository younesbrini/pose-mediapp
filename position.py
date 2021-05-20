import mediapipe as mp 
import os
mp_pose = mp.solutions.pose

import get_landmarks
import utils

class Position():
    """
    A Position is defined by how a person's body is located within a frame
    """
    def __init__(self, landmarks, image_w, image_h):
        self.width = image_w
        self.heigth = image_h
        self.landmarks = landmarks
        self.__get_keypoints()
        self.__get_angles()
    
    def __get_keypoints(self):
        self.keypoints = {}
        self.keypoints["LShoulder"]=[self.landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * self.width,self.landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * self.heigth]
        self.keypoints["RShoulder"]=[self.landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * self.width,self.landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * self.heigth]
        self.keypoints["LElbow"]=[self.landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * self.width,self.landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * self.heigth]
        self.keypoints["RElbow"]=[self.landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * self.width,self.landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * self.heigth]
        self.keypoints["LWrist"]=[self.landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * self.width,self.landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * self.heigth]    
        self.keypoints["RWrist"]=[self.landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x * self.width,self.landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y * self.heigth]    
        self.keypoints["LHip"]=[self.landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * self.width,self.landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * self.heigth]    
        self.keypoints["RHip"]=[self.landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x * self.width,self.landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y * self.heigth]   
        self.keypoints["LKnee"]=[self.landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x * self.width,self.landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y * self.heigth]   
        self.keypoints["RKnee"]=[self.landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x * self.width,self.landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y * self.heigth]
        self.keypoints["LAnkle"]=[self.landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x * self.width,self.landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y * self.heigth]
        self.keypoints["RAnkle"]=[self.landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x * self.width,self.landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y * self.heigth]

    def __get_angles(self):
        self.__angles = {}
        self.__angles['LShoulder'] = utils.calculate_angle(self.keypoints["LElbow"], self.keypoints["LShoulder"], self.keypoints["LHip"])
        self.__angles['RShoulder'] = utils.calculate_angle(self.keypoints["RElbow"], self.keypoints["RShoulder"], self.keypoints["RHip"])
        self.__angles['LElbow'] = utils.calculate_angle(self.keypoints["LWrist"], self.keypoints["LElbow"], self.keypoints["LShoulder"])
        self.__angles['RElbow'] = utils.calculate_angle(self.keypoints["RWrist"], self.keypoints["RElbow"], self.keypoints["RShoulder"])
        self.__angles['LHip'] = utils.calculate_angle(self.keypoints["LKnee"], self.keypoints["LHip"], self.keypoints["LShoulder"])
        self.__angles['RHip'] = utils.calculate_angle(self.keypoints["RKnee"], self.keypoints["RHip"], self.keypoints["RShoulder"])
        self.__angles['LKnee'] = utils.calculate_angle(self.keypoints["LAnkle"], self.keypoints["LKnee"], self.keypoints["LHip"])
        self.__angles['RKnee'] = utils.calculate_angle(self.keypoints["RAnkle"], self.keypoints["RKnee"], self.keypoints["RHip"])

    @property
    def angles(self):
        return self.__angles

class Asana(Position):
    """
    Asanas are yoga referenced positions.
    """
    def __init__(self, landmarks, image_w, image_h, name):
        self.name = name
        super().__init__(landmarks, image_w, image_h)
    
    #This is where we should put as an attribute of asanas the angles that matter for that asana
        
def load_asanas(dir_path):
    dir_path = os.getcwd()+'/src_asanas/'
    _, _, filenames = next(os.walk(dir_path))
    print(filenames)
    asana_dict={}
    for filename in filenames:
        if '.png' in filename or  '.jpg' in filename:
            landmarks, w, h = get_landmarks.extract_landmarks(dir_path + filename)
            asana_dict[filename]=Asana(landmarks, w, h, filename)
    return asana_dict

        
if __name__ == '__main__':
    # landmarks, w, h = get_landmarks.extract_landmarks('test1.jpg')
    # # pos1 = Position(landmarks, w, h)
    # # print(pos1.angles)
    # pos = Asana(landmarks, w, h, "Heyo")
    # print(pos.angles)
    path = os.getcwd()+'/src_asanas/'
    asana_dict = load_asanas(path)
    for name in asana_dict:
        print(asana_dict[name].angles)
