import cv2 as cv
from pathlib import Path
import numpy as np

def load_image_file(path: Path):
    try:
        return cv.imread(path)
    except:
        raise ImportError("Image not found in path {}".format(path))


def preprocess_image(image, convert_color: bool = True, horizontal_flip: bool = False):
    if horizontal_flip:
        image = cv.flip(image, 1)
    
    if convert_color:
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    return image


