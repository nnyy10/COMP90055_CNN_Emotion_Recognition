import keras
import tensorflow as tf
from keras.regularizers import l2
from keras.models import Model
from keras.layers import Input

def pretrained_facenet_inception_v1(print_summary=False):
    model_dir = 'model/keras/model/facenet_keras.h5'

    inception_v1_model = keras.models.load_model(model_dir)
    inception_v1_model._layers.pop()
    inception_v1_model._layers.pop()
    inception_v1_model._layers.pop()
    inception_v1_model._layers.pop()


    inception_v1_model.summary()

    x = keras.layers.GlobalAveragePooling2D()(inception_v1_model.layers[-1].output)
    y = keras.layers.Dense(4096, activation='relu', kernel_initializer='he_uniform')(x)
    z = keras.layers.Dense(7, activation='softmax')(y)
    model = Model(inputs=inception_v1_model.input, outputs=z)
    model.summary()
    if print_summary:
        print(model.summary())
    return model

def pretrained_facenet_inception_v1_svm(print_summary=False):
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

