from utils import *
import cv2
import tensorflow as tf
from keras.backend import set_session
from face_detection import *

global graph, model, sess
sess = tf.Session()
graph = tf.get_default_graph()
set_session(sess)

model = tf.keras.models.load_model("model/mode_v1.h5")


def predict(image):
    print('detecting faces...')
    faces = detect_faces(image)
    print('done \n')

    if len(faces) == 0:
        print("no face detected in image")
        return None

    # optional line to see the faces in the image
    # display_all_faces(image, faces)

    print('processing faces...')
    processed_faces = [process_face(image, face) for face in faces]
    processed_faces = np.array(processed_faces)
    print('done \n')

    # with graph.as_default():
    print('making predictions...')
    global sess, graph, model
    with graph.as_default():
        set_session(sess)
        predictions = model.predict(processed_faces)
    print('done \n')

    print(predictions)
    emotion = get_predicted_emotion(predictions[0])
    print('the predicted emotion is: ', emotion)

    return emotion
