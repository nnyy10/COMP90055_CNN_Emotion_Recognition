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
