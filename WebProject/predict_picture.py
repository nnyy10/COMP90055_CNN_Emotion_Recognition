from utils import *
import cv2
import tensorflow as tf
from keras.backend import set_session
from face_detection import *
import keras
from utils import get_predicted_emotion, get_predicted_emotion_dictionary
from data_processing import process_face
import numpy as np
import codecs, json

global graph, model, sess
sess = tf.Session()
graph = tf.get_default_graph()
set_session(sess)
model = keras.models.load_model("model/best_model.h5", compile=False)


def predict(image, img_only=False):
    faces = detect_faces(image)

    if len(faces) == 0:
        print("no face detected in image")
        if img_only:
            return None
        else:
            return None, None

    print('processing faces...')
    processed_faces_pair = [process_face(image, face, size=(160, 160)) for face in faces]

    if not img_only:
        cropped_face = np.array([pair[0] for pair in processed_faces_pair], dtype=object)
    processed_faces = np.array([pair[1] for pair in processed_faces_pair], dtype=object)

    print('making predictions...')
    global graph, model, sess
    with graph.as_default():
        set_session(sess)
        predictions = model.predict(processed_faces)


    print('the predicted emotion is: ', get_predicted_emotion(predictions[0]))
    face_emotion_prediction_dictionary = [get_predicted_emotion_dictionary(prediction) for prediction in predictions]

    if not img_only:
        result = []
        for i in range(len(face_emotion_prediction_dictionary)):
            result.append(json.dumps({"face": rgbToString(cropped_face[i]), "prediction": face_emotion_prediction_dictionary[i]}, cls=NumpyEncoder))

    boxed_image = image
    for i, face in enumerate(faces):
        x, y, w, h = getxywh(face)
        boxed_image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 165, 255), 2)
        face_emotion = face_emotion_prediction_dictionary[i][0]

        font_scale = 0.9
        font = cv2.FONT_HERSHEY_PLAIN
        # set the rectangle background to white
        rectangle_bgr = (255, 255, 255)
        text = str(i+1) + ". " + face_emotion["emotion"] + ": " + face_emotion["probability"]
        # get the width and height of the text box
        (text_width, text_height) = cv2.getTextSize(text, font, fontScale=font_scale, thickness=1)[0]
        text_offset_x = x
        text_offset_y = y - 1
        box_coords = ((text_offset_x, text_offset_y), (text_offset_x + text_width + 2, text_offset_y - text_height - 2))
        cv2.rectangle(image, box_coords[0], box_coords[1], rectangle_bgr, cv2.FILLED)
        cv2.putText(image, text, (text_offset_x, text_offset_y), font, fontScale=font_scale, color=(0, 165, 255), thickness=1)

    if img_only:
        return rgbToString(boxed_image)
    else:
        return rgbToString(boxed_image), result


def predict_upload(image):
    faces = detect_faces(image)

    if len(faces) == 0:
        print("no face detected in image")
        return None, None, None

    print('processing faces...')
    processed_faces_pair = [process_face(image, face, size=(160, 160)) for face in faces]

    cropped_face = np.array([pair[0] for pair in processed_faces_pair], dtype=object)
    processed_faces = np.array([pair[1] for pair in processed_faces_pair], dtype=object)

    print('making predictions...')
    global graph, model, sess
    with graph.as_default():
        set_session(sess)
        predictions = model.predict(processed_faces)

    print('the predicted emotion is: ', get_predicted_emotion(predictions[0]))
    face_emotion_prediction_dictionary = [get_predicted_emotion_dictionary(prediction) for prediction in predictions]

    result = []
    for i in range(len(face_emotion_prediction_dictionary)):
        result.append(json.dumps({"face": rgbToString(cropped_face[i]), "prediction": face_emotion_prediction_dictionary[i]}, cls=NumpyEncoder))

    boxed_image = image
    for i, face in enumerate(faces):
        x, y, w, h = getxywh(face)
        boxed_image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 165, 255), 2)
        face_emotion = face_emotion_prediction_dictionary[i][0]

        font_scale = 0.9
        font = cv2.FONT_HERSHEY_PLAIN
        # set the rectangle background to white
        rectangle_bgr = (255, 255, 255)
        text = str(i+1) + ". " + face_emotion["emotion"] + ": " + face_emotion["probability"]
        # get the width and height of the text box
        (text_width, text_height) = cv2.getTextSize(text, font, fontScale=font_scale, thickness=1)[0]
        text_offset_x = x
        text_offset_y = y - 1
        box_coords = ((text_offset_x, text_offset_y), (text_offset_x + text_width + 2, text_offset_y - text_height - 2))
        cv2.rectangle(image, box_coords[0], box_coords[1], rectangle_bgr, cv2.FILLED)
        cv2.putText(image, text, (text_offset_x, text_offset_y), font, fontScale=font_scale, color=(0, 165, 255), thickness=1)


    return rgbToString(boxed_image), result, face_emotion_prediction_dictionary
