import cv2
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from face_detection import getxywh



def process_face(image, face):
    box_x, box_y, box_w, box_h = getxywh(face)
    crop_img = image[box_y:box_y + box_h, box_x:box_x + box_w]
    gray_img = cv2.cvtColor(crop_img, cv2.COLOR_RGB2GRAY)
    resized = cv2.resize(gray_img, (160, 160))
    resized = np.true_divide(resized, 255)
    stacked_img = np.stack((resized,) * 3, axis=-1)
    return stacked_img


def get_predicted_emotion(emotion_array):
    emotion_int = np.argmax(emotion_array)
    if emotion_int == 0:
        return "Angry"
    elif emotion_int == 1:
        return "Disgust"
    elif emotion_int == 2:
        return "Fear"
    elif emotion_int == 3:
        return "Happy"
    elif emotion_int == 4:
        return "Sad"
    elif emotion_int == 5:
        return "Surprise"
    elif emotion_int == 6:
        return "Neutral"
    else:
        return "invalid emotion"
