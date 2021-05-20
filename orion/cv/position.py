import numpy as np
import mediapipe as mp

mp_pose = mp.solutions.pose
PoseLandmark = mp_pose.PoseLandmark

from orion.cv.math import calculate_angle

class Position(object):
    """
    A Position is defined by how a person's body is located within a frame
    """

    # define Keypoints Of Interet
    KOIs = [
        "LEFT_SHOULDER", "RIGHT_SHOULDER",
        "LEFT_ELBOW", "RIGHT_ELBOW",
        "LEFT_WRIST", "RIGHT_WRIST",
        "LEFT_HIP", "RIGHT_HIP",
        "LEFT_KNEE", "RIGHT_KNEE",
        "LEFT_ANKLE", "RIGHT_ANKLE",
    ]

    # define Angles of Interest
    AOIs = {
        "SHOULDER": ("ELBOW", "HIP"), 
        "ELBOW": ("WRIST", "SHOULDER"), 
        "HIP": ("SHOULDER", "KNEE"), 
        "KNEE": ("HIP", "ANKLE")
    }

    def __init__(self, landmarks, image_w, image_h):
        self.width = image_w
        self.height = image_h
        self.landmarks = landmarks

        self._init_keypoints()
        self._init_angles()

    def _extract_keypoint(self, landmark_name: str):
        landmark_value = PoseLandmark[landmark_name].value

        return [
            self.landmarks[landmark_value].x * self.width,
            self.landmarks[landmark_value].y * self.height,
        ]
    
    def _init_keypoints(self):
        self._keypoints = {}

        for keypoint_name in Position.KOIs:
            self._keypoints[keypoint_name] = self._extract_keypoint(keypoint_name)

    def _init_angles(self):
        self._angles = {}

        for (midpoint, endpoints) in Position.AOIs.items():
            for side in ["LEFT", "RIGHT"]:
                self._angles[f"{side}_{midpoint}"] = calculate_angle(
                    self._keypoints[f"{side}_{endpoints[0]}"], 
                    self._keypoints[f"{side}_{midpoint}"], 
                    self._keypoints[f"{side}_{endpoints[1]}"], 
                )

    @property
    def angles(self):
        return self._angles