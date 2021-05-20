from orion.utils import DATA_PATH
import os
import filetype
from pathlib import Path

import logging

from orion.cv.pose_landmark_estimator import PoseLandmarkEstimator
from orion.cv.utils import load_image_file

from orion.cv.asana.position import Asana

ASANA_TRAINING_IMAGES = DATA_PATH / "asana_training_images"

class AsanaClassifier:
    def __init__(self, dirpath: Path = ""):
        self._asanas = {}

        if dirpath != "":
            self.load_asanas_from_dir(dirpath=dirpath)

    def load_asanas_from_dir(self, dirpath: Path, **config):
        if os.path.isdir(dirpath) is not True:
            raise NotADirectoryError

        ple = PoseLandmarkEstimator(static_image_mode=True, **config)

        images = {}
        logging.info("Loading images from dir...")
        for filename in os.listdir(dirpath):
            if filetype.is_image(dirpath / filename):
                name = filename.split(".")[0]

                images[name] = load_image_file(dirpath / filename)

        asanas = {}
        logging.info("Estimating landmarks from images...")
        for name, image in self._images.items():
            landmarks = ple.predict(image)
            width, height, _ = image.shape

            asanas[name] = Asana(name, landmarks, width, height)

        self._asanas = asanas

    def predict(self, position):
        raise NotImplementedError



# def clasifier(position_test, position_test_flip, asana_dict):
#     """
#     Returns the most likely pose realized by the test position and the probability of the label
#     """
#     error_dict = {}
#     for name in asana_dict:
#         error_dict[name] = min(
#             calculate_distance_between_angles(position_test.angles, asana_dict[name].angles),
#             calculate_distance_between_angles(position_test_flip.angles, asana_dict[name].angles),
#         )
#         # I only did this for conveniance.
#         # It is horribly wrong as we can determine beforehand if we should flip the image or not beforehand
#     label = min(error_dict.keys(), key=(lambda k: error_dict[k]))

#     # Probability measure that is super biased based on the asanas selected, but better than nothing
#     clasifier_dict = {}
#     maxi = max(error_dict.values())
#     for key in error_dict:
#         clasifier_dict[key] = 1 - error_dict[key] / maxi
#     return (label, clasifier_dict[label])


# def maximum_error(position_angles, asana_angles):
#     maxi_error = 0
#     location = ""
#     for key in position_angles:
#         if maxi_error < abs(position_angles[key] - asana_angles[key]):
#             maxi_error = abs(position_angles[key] - asana_angles[key])
#             location = key
#     return maxi_error, location


# if __name__ == "__main__":
#     # MODEL ASANAS
#     dir_asana_path = os.getcwd() + "/src_asanas/"
#     asana_dict = load_asanas(dir_asana_path)

#     # TEST IMAGE
#     image_test_path = os.getcwd() + "/test/downdog_test.jpg"
#     landmarks, w, h = extract_landmarks(image_test_path)
#     flip_landmarks, w, h = extract_landmarks(image_test_path, flip=True)
#     position_test = Position(landmarks, w, h)
#     position_test_flip = Position(flip_landmarks, w, h)

#     # Clasify
#     label, proba = clasifier(position_test, position_test_flip, asana_dict)
#     print(
#         "The position realized is {} at a {} % probability ".format(
#             label, int(proba * 100)
#         )
#     )

#     # Error Max
#     maxi_error, location = maximum_error(position_test.angles, asana_dict[label].angles)
#     print(
#         "The yogi should pay attention to his {} and correct it at {} degrees".format(
#             location, int(maxi_error)
#         )
#     )
#     if position_test.angles[location] - asana_dict[label].angles[location] > 0:
#         correction = "close"
#     else:
#         correction = "open"

#     print(
#         "The yogi should {} his {} at {} degrees".format(
#             correction, location, int(maxi_error)
#         )
#     )
