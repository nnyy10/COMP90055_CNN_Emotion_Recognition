# -*- coding: utf-8 -*-
"""
face_detection module which is used to find the faces in an image.
"""

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
    """
    Given an RGB image, this function returns a list of json object each of which represents a face.
    The json object contains the coordinates of the face in the original image.
    """
    global graph, detector, sess
    with sess.graph.as_default():
        set_session(sess)
        face_list = detector.detect_faces(image)
        faces = [face["box"] for face in face_list]
        return faces


def getxywh(face):
    """
    util function to get the x, y, width and height from a face json object returned by the detect_face function.
    """
    return face[0], face[1], face[2], face[3]
