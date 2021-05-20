import os
from pathlib import Path
import cv2 as cv
import numpy as np
import mediapipe as mp

# from position import load_asanas, Position, Asana
# from clasifier import clasifier, maximum_error

mp_pose = mp.solutions.pose

from orion.cv.math import calculate_angle, calculate_distance_between_angles
from orion.cv.utils import preprocess_image


class PoseLandmarkEstimator(object):
    def __init__(
        self,
        static_image_mode=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        model_complexity=1,
        **config
    ):
        self._pose = mp_pose.Pose(
            static_image_mode=static_image_mode,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            model_complexity=model_complexity,
        )

    def predict(self, image):
        image = preprocess_image(image)

        results = self._pose.process(image)

        return results.pose_landmarks.landmark