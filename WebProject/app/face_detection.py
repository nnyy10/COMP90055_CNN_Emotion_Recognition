from mtcnn import MTCNN
import tensorflow as tf
from keras.backend import set_session


global graph, model, sess

graph = tf.get_default_graph()
sess = tf.Session(graph=graph)
with sess.graph.as_default():
    set_session(sess)
    detector = MTCNN()


def detect_faces(image):
    global graph, detector, sess
    with sess.graph.as_default():
        set_session(sess)
        face_list = detector.detect_faces(image)
        faces = [face["box"] for face in face_list]
        return faces


def getxywh(face):
    return face[0], face[1], face[2], face[3]
