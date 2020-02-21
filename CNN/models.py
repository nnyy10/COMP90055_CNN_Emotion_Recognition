# -*- coding: utf-8 -*-
"""
All keras models including all variations to inception-resnet and mobilenet v2
"""

import keras
import tensorflow as tf
from keras.regularizers import l2
from keras.models import Model
from keras.layers import Input


def pretrained_facenet_inception_v1(print_summary=False):
    """
    base inception-resent model loaded from pre-trained weights
    """
    model_dir = 'model/keras/model/facenet_keras.h5'

    inception_v1_model = keras.models.load_model(model_dir)
    model = keras.Sequential()
    model.add(inception_v1_model)
    model.add(keras.layers.Dense(7, activation='softmax'))
    if print_summary:
        print(model.summary())
    return model

def pretrained_facenet_inception_v1_modified(print_summary=False):
    """
    inception-resnet with the last layers being dropout layer and bottleneck layer replaced with 2 fully connected
    dense layer.
    """
    model_dir = 'model/keras/model/facenet_keras.h5'

    inception_v1_model = keras.models.load_model(model_dir)
    inception_v1_model._layers.pop()
    inception_v1_model._layers.pop()
    inception_v1_model._layers.pop()
    inception_v1_model._layers.pop()


    x = keras.layers.GlobalAveragePooling2D()(inception_v1_model.layers[-1].output)
    y = keras.layers.Dense(4096, activation='relu', kernel_initializer='he_uniform')(x)
    z = keras.layers.Dense(7, activation='softmax')(y)
    model = Model(inputs=inception_v1_model.input, outputs=z)
    if print_summary:
        print(model.summary())
    return model

def pretrained_facenet_inception_v1_svm(print_summary=False):
    """
    inception-resnet with the loss function being that similar to the SVM with l2 kernel regularizer.
    """
    model_dir = 'model/keras/model/facenet_keras.h5'

    inception_v1_model = keras.models.load_model(model_dir)
    model = keras.Sequential()
    model.add(inception_v1_model)
    model.add(keras.layers.Dense(7, kernel_regularizer=l2(0.01)))
    model.add(keras.layers.Activation('softmax'))
    if print_summary:
        print(model.summary())
    return model



def pretrained_mobilenet(print_summary=False):
    """
    Mobilenetv2 model pre-trained on imagenet.
    """
    mobilenet = keras.applications.MobileNetV2(input_shape=(48, 48, 3),
                                               include_top=False,
                                               weights='imagenet')
    model = keras.Sequential()
    model.add(mobilenet)
    model.add(keras.layers.GlobalAveragePooling2D())
    model.add(keras.layers.Dense(7, activation='softmax'))
    if print_summary:
        print(model.summary())
    return model

