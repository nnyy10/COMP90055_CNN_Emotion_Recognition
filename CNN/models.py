import keras


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
    model.add(keras.layers.Dense(7, activation='softmax'))
    if print_summary:
        print(model.summary())
    return model
