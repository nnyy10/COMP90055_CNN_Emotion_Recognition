# -*- coding: utf-8 -*-
"""
Module that takes the preprocessed data in data/processed_data/(cropped or raw) and loads the pre trained models
defined in model.py and starts training it. Afterwards saving the model in model/keras/model/ as well as a log file in
log/.

Different hyper-parameters can be defined in the beginning of the script such as epoch, batchsize, loss function etc.

NOTE: This script is depreciated and the train_batches should be used instead. This script is unable to do data
augmentation while train_batch.py is.
"""

import numpy as np
import tensorflow as tf
import keras
from os import path
from utils import load_data_from_npy, y_single_to_list, plot_loss_history, plot_acc_history, get_confusion_matrix
from data_processing import format_x
from models import *
import tensorflow_datasets as tfds
import logging
import os

BATCH_SIZE = 64
EPOCH = 4
OPTIMIZER = keras.optimizers.RMSprop(lr=0.00001)
LOSS_FUNCTION = tf.keras.losses.categorical_crossentropy
SAVE_MODEL = True
PLOT_TRAINING_HISTORY = False
PRINT_CONFUSION_MATRIX = True
LOG = True

model_initializer = pretrained_facenet_inception_v1
model = model_initializer(print_summary=False)

# ka = kaggle, uc = uncropped
DATA_SET_NAME = "KAUC"
# if you wish to give the model an ID
MODEL_NAME_ID = ""

print('reading data...')
data_directory = "data/processed_data/raw"
x_train, y_train, x_valid, y_valid, x_test, y_test = load_data_from_npy(data_directory)
print('done \n')

print('processing data...')
x_train = np.array([format_x(x, resize=(160, 160), expand_dimension=True, normalize=True) for x in x_train])
x_valid = np.array([format_x(x, resize=(160, 160), expand_dimension=True, normalize=True) for x in x_valid])
x_test = np.array([format_x(x, resize=(160, 160), expand_dimension=True, normalize=True) for x in x_test])
y_train = y_single_to_list(y_train)
y_valid = y_single_to_list(y_valid)
y_test = y_single_to_list(y_test)
print('done \n')

print('compiling model...')
model.compile(optimizer=OPTIMIZER, metrics=['accuracy'], loss=LOSS_FUNCTION)
print('done \n')

print('fitting model... ')
history = model.fit(x_train, y_train, batch_size=BATCH_SIZE, epochs=EPOCH, verbose=1, validation_data=(x_valid, y_valid))
print('done \n')

test_result = model.evaluate(x_test, y_test)
y_predicted = model.predict(x_test)
print("\nTest loss and accuracy: ", test_result)

# ----------------------------------------------------------------------------
"""Saving model and logging"""
print("Saving model and logging...")
MODEL_NAME = "DA{0}_BS{1}_EP{2}_OP{3}_LO{4}_MO{5}_TRA{6}_TEA{7}{8}_WA".format(DATA_SET_NAME,
                                                                                          str(int(BATCH_SIZE)),
                                                                                          str(int(EPOCH)),
                                                                                          OPTIMIZER.__class__.__name__,
                                                                                          LOSS_FUNCTION.__name__,
                                                                                          model_initializer.__name__,
                                                                                          str(int(
                                                                                              history.history['accuracy'][-1] * 100)),
                                                                                          str(int(
                                                                                              test_result[1] * 100)),
                                                                                          MODEL_NAME_ID)

if SAVE_MODEL:
    save_model_dir = "model/keras/model/"
    SAVE_MODEL_NAME = MODEL_NAME + ".h5"
    model.save(path.join(save_model_dir, SAVE_MODEL_NAME))

if LOG:
    LOG_FILE_NAME = MODEL_NAME + ".log"
    LOG = os.path.join("log", LOG_FILE_NAME)
    logging.basicConfig(filename=LOG, filemode="w", level=logging.INFO)
    logging.info("Data: " + DATA_SET_NAME)
    logging.info("Batch Size: " + str(int(BATCH_SIZE)))
    logging.info("EPOCH number: " + str(int(EPOCH)))
    logging.info("Optimizer: " + OPTIMIZER.__class__.__name__)
    logging.info("Loss Function: " + LOSS_FUNCTION.__name__)
    logging.info("Base Model: " + LOSS_FUNCTION.__name__)
    logging.info("Train Accuracy: " + str(round(history.history['accuracy'][-1] * 100, 2)))
    logging.info("Test Accuracy: " + str(round(test_result[1] * 100, 2)))
    logging.info("Train Accuracy History: " + str([round(x*100, 2) for x in history.history['accuracy']]))
    logging.info("Validation Accuracy History: " + str([round(x*100, 2) for x in history.history['val_accuracy']]))
    logging.info("Train Loss History: " + str([round(x, 4) for x in history.history['loss']]))
    logging.info("Validation Loss History: " + str([round(x, 4) for x in history.history['val_loss']]))
    logging.info("")
    logging.info("")
    logging.info(get_confusion_matrix(y_actual=y_test, y_predicted=y_predicted))

if PLOT_TRAINING_HISTORY:
    plot_acc_history(history)
    plot_loss_history(history)
