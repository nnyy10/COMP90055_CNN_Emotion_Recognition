import cv2
from mtcnn import MTCNN
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.backend import set_session


def getxywh(face):
    return face[0], face[1], face[2], face[3]


def display_all_faces(image, faces):
    for face in faces:
        box_x, box_y, box_w, box_h = getxywh(face)
        image = cv2.rectangle(image, (box_x, box_y), (box_x + box_w, box_y + box_h), (255, 0, 0))

    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()
