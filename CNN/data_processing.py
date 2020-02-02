import cv2
import numpy as np
from mtcnn import MTCNN


def emotion_int_to_str(emotion_int):
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
        return None


def emotion_str_to_int(emotion_str):
    if emotion_str.lower() == "angry":
        return 0
    elif emotion_str.lower() == "disgust":
        return 1
    elif emotion_str.lower() == "fear":
        return 2
    elif emotion_str.lower() == "happy":
        return 3
    elif emotion_str.lower() == "sad":
        return 4
    elif emotion_str.lower() == "surprise":
        return 5
    elif emotion_str.lower() == "neutral":
        return 6
    else:
        return None

detector = MTCNN()


def detect_faces(image):
    global detector
    faces = [face["box"] for face in detector.detect_faces(image)]
    return faces


def getxywh(face):
    return face[0], face[1], face[2], face[3]


def crop_face_single(pixel_array, resize=True):
    if pixel_array.ndim == 3:
        y, x, channel = pixel_array.shape
    else:
        y, x = pixel_array.shape

    if pixel_array.ndim == 2:
        pixel_original = pixel_array
        pixel_array = np.stack((pixel_array,) * 3, axis=-1)

    faces = detect_faces(pixel_array)

    if pixel_array.ndim == 2:
        pixel_array = pixel_original

    if len(faces) != 1:
        return pixel_array
    box_x, box_y, box_w, box_h = getxywh(faces[0])

    y_start = box_y
    y_end = box_y + box_h
    x_start = box_x
    x_end = box_x + box_w
    if y_start < 0:
        y_start = 0
    if x_start < 0:
        x_start = 0
    if y_end > y-1:
        y_end = y-1
    if x_end > y-1:
        x_end = y-1
    crop_img = pixel_array[y_start:y_end, x_start:x_end]

    if resize:
        return cv2.resize(crop_img, (x, y))
    else:
        return crop_img
