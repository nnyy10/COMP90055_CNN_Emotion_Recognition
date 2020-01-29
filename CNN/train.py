import csv
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import keras
import cv2
import scipy
import os
import pycm


print('reading data...')

base_image_path = 'data/processed_data'
image_type_path = 'base'

x_train = np.load(os.path.join(base_image_path, image_type_path, 'x_train.npy'))
# x_train_new = []
# for x in x_train:
#     x_train_new.append(cv2.resize(x, (160, 160)))
# x_train = np.array(x_train_new)
x_train = np.true_divide(x_train, 255)

x_test_new = []
x_test = np.load(os.path.join(base_image_path, image_type_path, 'x_test.npy'))
# for x in x_test:
#     x_test_new.append(cv2.resize(x, (160, 160)))
# x_test = np.array(x_test_new)
x_test = np.true_divide(x_test, 255)

x_valid_new = []
x_valid = np.load(os.path.join(base_image_path, image_type_path, 'x_valid.npy'))
# for x in x_valid:
#     x_valid_new.append(cv2.resize(x, (160, 160)))
# x = np.array(x_valid_new)
x_valid = np.true_divide(x_valid, 255)

y_train = np.load(os.path.join(base_image_path, image_type_path, 'y_train.npy'))
y_test = np.load(os.path.join(base_image_path, image_type_path, 'y_test.npy'))
y_valid = np.load(os.path.join(base_image_path, image_type_path, 'y_valid.npy'))
print('done \n')

print('creating model...')
model_dir = 'model/keras/model/facenet_keras.h5'

inception_v1_model = keras.models.load_model(model_dir)

print(inception_v1_model.summary())

# for layer in inception_v1_model.layers:
#     layer.trainable = False

model = keras.Sequential()

model.add(inception_v1_model)
model.add(keras.layers.Dense(7, activation='softmax'))
print(model.summary())



model.compile(keras.optimizers.RMSprop(lr=0.00001), metrics=['accuracy'], loss=tf.keras.losses.categorical_crossentropy)
print('done \n')

print('fitting model... ')
model.fit(x_train, y_train, batch_size=64, epochs=1, verbose=1, validation_data=(x_valid, y_valid))
print('done \n')

# model.save('mode_v2.h5')
print(model.evaluate(x_test, y_test))

y_predicted = model.predict(x_test)
y_actual = y_test

y_predicted = map(np.argmax, y_predicted)
y_actual = map(np.argmax, y_test)

cm = pycm.ConfusionMatrix(actual_vector=y_actual, predict_vector=y_predicted)
print(cm)



