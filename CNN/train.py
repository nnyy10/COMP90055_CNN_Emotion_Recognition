import csv
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import keras
import cv2
import scipy
import os
import pycm
from utils import *
from keras.applications.nasnet import NASNetLarge


print('reading data...')
x_train, y_train, x_valid, y_valid, x_test, y_test = load_data()
print(x_train.shape)
print('done \n')

print('creating model...')
model = create_model()
print(model.summary())
print('model_created')

print('fitting model... ')
history = model.fit(x_train, y_train, batch_size=64, epochs=4, verbose=1, validation_data=(x_valid, y_valid))
print('done \n')
#
#
# # model.save('mode_v2.h5')
# print(model.evaluate(x_test, y_test))
#
# plot_acc_history(history)
# plot_loss_history(history)
#
# # cm = pycm.ConfusionMatrix(actual_vector=y_actual, predict_vector=y_predicted)
# # print(cm)
#


