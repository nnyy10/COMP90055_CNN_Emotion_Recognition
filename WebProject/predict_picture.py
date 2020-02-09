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


def predict(image):
    faces = detect_faces(image)
    # with graph.as_default():

    if len(faces) == 0:
        print("no face detected in image")
        return None


    print('processing faces...')
    processed_faces_pair = [process_face(image, face, size=(160, 160)) for face in faces]
    cropped_face = np.array([pair[0] for pair in processed_faces_pair])
    processed_faces = np.array([pair[1] for pair in processed_faces_pair])
    print('done \n')

    print('making predictions...')
    global graph, model, sess
    with graph.as_default():
        set_session(sess)
        predictions = model.predict(processed_faces)
    print('done \n')

    print('the predicted emotion is: ', get_predicted_emotion(predictions[0]))
    face_emotion_prediction_dictionary = [get_predicted_emotion_dictionary(prediction) for prediction in predictions]

    result = []
    for i in range(len(face_emotion_prediction_dictionary)):
        cropped_face_list = cropped_face.tolist()
        result.append(json.dumps({"face": cropped_face, "prediction": face_emotion_prediction_dictionary}, cls=NumpyEncoder))

    # print(face_emotion_prediction_dictionary)
    # print(face_emotion_prediction_dictionary)
    # return face_emotion_prediction_dictionary[0][1]
    return result
