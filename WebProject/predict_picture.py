from utils import *
import cv2
import tensorflow as tf
from keras.backend import set_session
# from face_detection import *
import keras

global graph
global model
global sess
sess = tf.Session()
graph = tf.get_default_graph()
set_session(sess)
model = keras.models.load_model("model/best_model.h5", compile=False)


def predict(image):
    processed_faces = np.array([cv2.resize(image,(160, 160))])
    # with graph.as_default():
    print('making predictions...')
    with graph.as_default():
        set_session(sess)
        predictions = model.predict(processed_faces)
    print('done \n')

    print(predictions)
    emotion = get_predicted_emotion(predictions[0])
    print('the predicted emotion is: ', emotion)

    return emotion
