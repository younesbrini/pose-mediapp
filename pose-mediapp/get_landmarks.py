import mediapipe as mp
import cv2 as cv

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5, model_complexity=2)

def extract_landmarks(path='test1.jpg',flip=False):
  try:
    image = cv.imread(path)
    if flip == True:
      image = cv.flip(image, 1)
    results = pose.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    image_height, image_width, _ = image.shape
  except:
    raise ImportError("Images not found in path {}".format(path))
  return (results.pose_landmarks.landmark, image_width, image_height)

