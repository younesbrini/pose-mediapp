
from orion.cv.position import Position


class Asana(Position):
    """
    Asanas are yoga referenced positions.
    """
    def __init__(self, name : str, landmarks, image_w, image_h):
        self.name = name
        super().__init__(landmarks, image_w, image_h)

    #This is where we should put as an attribute of asanas the angles that matter for that asana
        