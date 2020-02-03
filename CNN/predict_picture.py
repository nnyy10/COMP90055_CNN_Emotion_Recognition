import cv2
from data_processing import process_face
from face_detection import display_all_faces
import numpy as np
import tensorflow as tf
from utils import get_predicted_emotion, get_predicted_emotion_dictionary

model = tf.keras.models.load_model("model/keras/model/mode_v1.h5")


def predict(image):
    print('Reading image...')
    image_path = 'data/images/gettyimages-514325215-612x612.jpg'
    image = cv2.imread(image_path)
    print('done \n')

    print('detecting faces...')
    from face_detection import detect_faces
    faces = detect_faces(image)
    print('done \n')

    if len(faces) == 0:
        print("no face detected in image")
        return None

    # # optional line to see the faces in the image
    # display_all_faces(image, faces)

    print('processing faces...')
    processed_faces_pair = [process_face(image, face, size=(160, 160)) for face in faces]
    cropped_face = np.array([pair[0] for pair in processed_faces_pair])
    processed_faces = np.array([pair[1] for pair in processed_faces_pair])
    print('done \n')

    print('making predictions...')
    predictions = model.predict(processed_faces)
    print('done \n')

    print('the predicted emotion is: ', get_predicted_emotion(predictions[0]))
    face_emotion_prediction_dictionary = [get_predicted_emotion_dictionary(prediction) for prediction in predictions]
    return list(zip(cropped_face, face_emotion_prediction_dictionary))


result = predict(None)
if result != None:
    print(result[0])