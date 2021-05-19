import mediapipe as mp
import cv2 as cv

mp_pose = mp.solutions.pose

def extract_landmarks(path='test1.jpg'):
  image = cv.imread(path)
  pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5, model_complexity=2)
  # Convert the BGR image to RGB and process it with MediaPipe Pose.
  results = pose.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))
  # Print nose landmark.
  image_height, image_width, _ = image.shape
  # if not results.pose_landmarks:
  #   continue

  return (results.pose_landmarks.landmark, image_width, image_height)
