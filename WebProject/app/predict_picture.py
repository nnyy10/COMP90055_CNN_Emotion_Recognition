import tensorflow as tf
import utils
from face_detection import detect_faces
import keras
import numpy as np
from keras.backend import set_session

global graph, inception_resnet_model, mobilenetv2_model, sess
sess = tf.Session()
graph = tf.get_default_graph()
set_session(sess)
inception_resnet_model = keras.models.load_model("model/final_inception_resnet.h5", compile=False)
mobilenetv2_model = keras.models.load_model("model/final_mobilenetv2.h5", compile=False)


def predict(image, model_to_use="inception-resnet"):
    faces = detect_faces(image)

    if len(faces) == 0:
        print("no face detected in image")
        return {"found": False}

    print('processing faces...')
    if model_to_use == "mobilenetv2":
        size = (48, 48)
    else:
        size = (160, 160)
    processed_faces_pair = [utils.process_face(image, face, size=size) for face in faces]
    cropped_face = np.array([pair[0] for pair in processed_faces_pair], dtype=object)
    processed_faces = np.array([pair[1] for pair in processed_faces_pair], dtype=object)

    print('making predictions...')
    global graph, inception_resnet_model, mobilenetv2_model, sess
    with graph.as_default():
        set_session(sess)
        if model_to_use == "mobilenetv2":
            predictions = mobilenetv2_model.predict(processed_faces)
        else:
            predictions = inception_resnet_model.predict(processed_faces)

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


def predict_upload(image, model_to_use="inception-resnet"):
    faces = detect_faces(image)

    if len(faces) == 0:
        print("no face detected in image")
        return None, None, None, None

    print('processing faces...')
    if model_to_use == "mobilenetv2":
        size = (48, 48)
    else:
        size = (160, 160)
    processed_faces_pair = [utils.process_face(image, face, size=size) for face in faces]

    cropped_face = np.array([pair[0] for pair in processed_faces_pair], dtype=object)
    processed_faces = np.array([pair[1] for pair in processed_faces_pair], dtype=object)

    print('making predictions...')
    global graph, inception_resnet_model, mobilenetv2_model, sess
    with graph.as_default():
        set_session(sess)
        if model_to_use == "mobilenetv2":
            predictions = mobilenetv2_model.predict(processed_faces)
        else:
            predictions = inception_resnet_model.predict(processed_faces)

    face_emotion_prediction_dictionary = [utils.get_predicted_emotion_dictionary(prediction) for prediction in predictions]

    result = []
    for i in range(len(face_emotion_prediction_dictionary)):
        face_buffer = utils.rgb_to_buffer(cropped_face[i])
        face_base64_string = utils.buffer_to_base64_string(face_buffer)
        result.append({"face": face_base64_string, "prediction": face_emotion_prediction_dictionary[i]})

    cropped_face_buff = [utils.rgb_to_buffer(face) for face in cropped_face]

    boxed_image = utils.draw_bounding_boxes(image, faces, face_emotion_prediction_dictionary)
    boxed_image_buffer = utils.rgb_to_buffer(boxed_image)
    boxed_image_base64_string = utils.buffer_to_base64_string(boxed_image_buffer)

    message = {"image": boxed_image_base64_string, "found": True, "faces": result}

    return message, face_emotion_prediction_dictionary, boxed_image_buffer, cropped_face_buff


def predict_img_only(image):
    faces = detect_faces(image)

    if len(faces) == 0:
        return {"found": False}

    processed_faces_pair = [utils.process_face(image, face, size=(160, 160)) for face in faces]
    processed_faces = np.array([pair[1] for pair in processed_faces_pair], dtype=object)

    global graph, inception_resnet_model, sess
    with graph.as_default():
        set_session(sess)
        predictions = inception_resnet_model.predict(processed_faces)

    face_emotion_prediction_dictionary = [utils.get_predicted_emotion_dictionary(prediction) for prediction in predictions]
    boxed_image = utils.draw_bounding_boxes(image, faces, face_emotion_prediction_dictionary)
    boxed_image_buffer = utils.rgb_to_buffer(boxed_image)
    boxed_image_base64_string = utils.buffer_to_base64_string(boxed_image_buffer)

    return {"image": boxed_image_base64_string, "found": True}

