import tensorflow as tf
import utils
from face_detection import detect_faces
import keras
import numpy as np
from keras.backend import set_session
import cv2

global graph, model, sess
sess = tf.Session()
graph = tf.get_default_graph()
set_session(sess)
model = keras.models.load_model("model/final_inception_resnet.h5", compile=False)


def predict(image):
    faces = detect_faces(image)

    if len(faces) == 0:
        print("no face detected in image")
        return {"found": False}

    print('processing faces...')
    processed_faces_pair = [utils.process_face(image, face, size=(160, 160)) for face in faces]
    cropped_face = np.array([pair[0] for pair in processed_faces_pair], dtype=object)
    processed_faces = np.array([pair[1] for pair in processed_faces_pair], dtype=object)

    print('making predictions...')
    global graph, model, sess
    with graph.as_default():
        set_session(sess)
        predictions = model.predict(processed_faces)

    face_emotion_prediction_dictionary = [utils.get_predicted_emotion_dictionary(prediction) for prediction in predictions]

    result = []
    for i in range(len(face_emotion_prediction_dictionary)):
        face_buffer = utils.rgb_to_buffer(cropped_face[i])
        face_base64_string = utils.buffer_to_base64_string(face_buffer)
        face_json = {"face": face_base64_string, "prediction": face_emotion_prediction_dictionary[i]}
        result.append(face_json)

    boxed_image = utils.draw_bounding_boxes(image, faces, face_emotion_prediction_dictionary)

    boxed_image_buffer = utils.rgb_to_buffer(boxed_image)
    boxed_image_base64_string = utils.buffer_to_base64_string(boxed_image_buffer)

    return {"image": boxed_image_base64_string, "found": True, "faces": result}


def predict_upload(image):
    faces = detect_faces(image)

    if len(faces) == 0:
        print("no face detected in image")
        return None, None, None, None

    print('processing faces...')
    processed_faces_pair = [utils.process_face(image, face, size=(160, 160)) for face in faces]

    cropped_face = np.array([pair[0] for pair in processed_faces_pair], dtype=object)
    processed_faces = np.array([pair[1] for pair in processed_faces_pair], dtype=object)

    print('making predictions...')
    global graph, model, sess
    with graph.as_default():
        set_session(sess)
        predictions = model.predict(processed_faces)

    face_emotion_prediction_dictionary = [utils.get_predicted_emotion_dictionary(prediction) for prediction in predictions]

    result = []
    for i in range(len(face_emotion_prediction_dictionary)):
        result.append({"face": utils.rgbToString(cropped_face[i])[0], "prediction": face_emotion_prediction_dictionary[i]})

    cropped_face_buff = [utils.rgbToString(face)[1] for face in cropped_face]

    boxed_image = utils.draw_bounding_boxes(image, faces, face_emotion_prediction_dictionary)

    return utils.rgbToString(boxed_image), result, face_emotion_prediction_dictionary, cropped_face_buff
