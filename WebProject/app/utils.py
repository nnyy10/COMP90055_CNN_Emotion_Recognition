# -*- coding: utf-8 -*-
"""
This utils module contains all the utilities function needed to make the website run.

Most of the functions are for image conversion. Other functions used for data processing and drawing bounding boxes.
"""

import base64
import io
import cv2
import numpy as np
from collections import Counter
from PIL import Image
from face_detection import getxywh


"""These two variables are needed for data preprocessing if the model is trained with data standardization and 
normalization """
data_mean = 0.5077424916139078
data_std = 0.25016892401139035



def process_face(image, face, size):
    """
    process_face crops a face from the original image as well as processing it so it is ready for prediction.
    """
    box_x, box_y, box_w, box_h = getxywh(face)
    y, x, z = image.shape
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
    if x_end > x-1:
        x_end = x-1

    cropped_face = image[y_start:y_end, x_start:x_end]
    processed_face = cv2.cvtColor(cropped_face, cv2.COLOR_RGB2GRAY)
    processed_face = cv2.resize(processed_face, size)
    processed_face = np.true_divide(processed_face, 255)
    # processed_face = np.subtract(processed_face, data_mean)
    # processed_face = np.true_divide(processed_face, data_std)
    processed_face = np.stack((processed_face,) * 3, axis=-1)
    return cropped_face, processed_face


emotions = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]


def emotion_int_to_str(emotion_int):
    return emotions[emotion_int]


def emotion_str_to_int(emotion_str):
    if emotion_str.lower() == "angry":
        return 0
    elif emotion_str.lower() == "disgust":
        return 1
    elif emotion_str.lower() == "fear":
        return 2
    elif emotion_str.lower() == "happy":
        return 3
    elif emotion_str.lower() == "neutral":
        return 4
    elif emotion_str.lower() == "sad":
        return 5
    elif emotion_str.lower() == "surprise":
        return 6
    else:
        return None


def get_predicted_emotion(emotion_array):
    emotion_int = np.argmax(emotion_array)
    return emotion_int_to_str(emotion_int)


def get_predicted_emotion_dictionary(emotion_array):
    emotion_structured = []
    for i in range(7):
        emotion_structured.append({"emotion": emotion_int_to_str(i), "probability": str(round(emotion_array[i], 2))})
    emotion_structured = sorted(emotion_structured, key=lambda x: x['probability'], reverse=True)
    return emotion_structured


def y_single_to_list(y_single):
    new_y_list = []
    for y in y_single:
        new_y = np.zeros(7)
        new_y[y] = 1
        new_y_list.append(new_y)
    return np.asarray(new_y_list)


def y_list_to_single(y_list):
    return np.asarray(list(map(np.argmax, y_list)))


def get_class_num(y_list):
    result = Counter(y_list)
    class_counter = [result[x] for x in range(7)]
    return np.asarray(class_counter)


def base64_to_rgb(base64_string):
    img_data = base64.b64decode(str(base64_string))
    image = Image.open(io.BytesIO(img_data))
    return np.array(image)


def rgb_to_buffer(rgb_array):
    pil_img = Image.fromarray(rgb_array.astype('uint8'))

    buff = io.BytesIO()
    pil_img.save(buff, format="JPEG")
    return buff.getvalue()


def buffer_to_base64_string(buffer):
    return base64.b64encode(buffer).decode("utf-8")


def rgb_to_pil(rgb_img):
    return Image.fromarray(rgb_img)


def pil_to_rgb(pil_img):
    return np.array(pil_img)


def base64_to_pil(base64_string):
    img_data = base64.b64decode(str(base64_string))
    return Image.open(io.BytesIO(img_data))


def draw_bounding_boxes(image, faces, face_emotion_prediction_dictionary):
    """
    draws the bounding boxes in the image
    """
    for i, face in enumerate(faces):
        x, y, w, h = getxywh(face)
        image = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 165, 0), 2)
        face_emotion = face_emotion_prediction_dictionary[i][0]
        font_scale = 0.9
        font = cv2.FONT_HERSHEY_PLAIN
        rectangle_bgr = (255, 255, 255)
        text = str(i+1) + ". " + face_emotion["emotion"] + ": " + face_emotion["probability"]
        (text_width, text_height) = cv2.getTextSize(text, font, fontScale=font_scale, thickness=1)[0]
        text_offset_x = x
        text_offset_y = y - 1
        box_coords = ((text_offset_x, text_offset_y), (text_offset_x + text_width + 2, text_offset_y - text_height - 2))
        cv2.rectangle(image, box_coords[0], box_coords[1], rectangle_bgr, cv2.FILLED)
        cv2.putText(image, text, (text_offset_x, text_offset_y), font, fontScale=font_scale, color=(255, 165, 0), thickness=1)
    return image
