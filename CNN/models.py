import keras
import tensorflow as tf

def pretrained_facenet_inception_v1(print_summary=False):
    model_dir = 'model/keras/model/facenet_keras.h5'

    inception_v1_model = keras.models.load_model(model_dir)
    model = keras.Sequential()
    model.add(inception_v1_model)
    model.add(keras.layers.Dense(7, activation='softmax'))
    if print_summary:
        print(model.summary())
    return model


def pretrained_NASNET(print_summary=False):
    NASNET_model = keras.applications.nasnet.NASNetLarge(input_shape=(331, 331, 3),
                                                  include_top=False,
                                                  weights="imagenet",
                                                  pooling=None)

    model = keras.Sequential()
    model.add(NASNET_model)
    model.add(keras.layers.GlobalAveragePooling2D())
    model.add(keras.layers.Dense(7, activation='softmax'))
    if print_summary:
        print(model.summary())
    return model

def pretrained_xception(print_summary=False):
    xceptionmodel = keras.applications.xception.Xception(input_shape=(96, 96, 3),include_top=False,weights='imagenet')
    model = keras.Sequential()
    model.add(xceptionmodel)
    model.add(keras.layers.GlobalAveragePooling2D())
    model.add(keras.layers.Dense(7, activation=None))
    model.add(keras.layers.Lambda(lambda x: tf.math.l2_normalize(x, axis=1)))  # L2 normalize embeddings
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

