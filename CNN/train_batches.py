# -*- coding: utf-8 -*-
"""
Module that takes the preprocessed data in data/processed_data/(cropped_img or raw_img) and loads the pre trained models
defined in model.py and starts training it. Afterwards saving the model in model/keras/model/ as well as a log file in
log/.

Different hyper-parameters can be defined in the beginning of the script such as epoch, batchsize, loss function etc.
"""

# ----------------------------------------------------------------------------
"""Import modules"""
import numpy as np
import tensorflow as tf
import keras
from os import path

from data_processing import format_x
from utils import plot_loss_history, plot_acc_history, get_confusion_matrix, load_data_from_npy
from models import *
from keras.preprocessing.image import ImageDataGenerator
import logging
import os
from collections import Counter
from sklearn.utils import class_weight


# ----------------------------------------------------------------------------
"""Set training parameters"""
BATCH_SIZE = 64
EPOCH = 30
OPTIMIZER = keras.optimizers.RMSprop(lr=0.001)
LOSS_FUNCTION = tf.keras.losses.categorical_crossentropy
SAVE_MODEL = True
LOG = True
PLOT_TRAINING_HISTORY = False

print("loading model...")
model_initializer = pretrained_mobilenet
model = model_initializer(print_summary=False)
print("done \n")

# ka = kaggle, uc = uncropped
DATA_SET_NAME = "kac"
# if you wish to give the model a unique ID
MODEL_NAME_ID = ""

IMG_SIZE = (48, 48)


# ----------------------------------------------------------------------------
"""Load data"""
print('creating data generator')

def preprocess(nparr):
    result = np.subtract(nparr, 0.5077424916139078)
    result = np.true_divide(result, 0.25016892401139035)
    return result


train_datagen = ImageDataGenerator(rescale=1. / 255,
                                   rotation_range=45,
                                   width_shift_range=0.2,
                                   height_shift_range=0.2,
                                   brightness_range=[0.5, 1.5],
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True,
                                   featurewise_center=True,
                                   featurewise_std_normalization=True,
                                   preprocessing_function=preprocess)

test_datagen = ImageDataGenerator(rescale=1. / 255,
                                  featurewise_center=True,
                                  featurewise_std_normalization=True,
                                  preprocessing_function=preprocess)

TRAIN_DIR = "data/processed_data/cropped_img/train"
VALID_DIR = "data/processed_data/cropped_img/valid"
TEST_DIR = "data/processed_data/cropped_img/test"
train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE)

validation_generator = test_datagen.flow_from_directory(
    VALID_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE)

label_map = (validation_generator.class_indices)
print(label_map)
test_generator = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE, shuffle=False)
print('done \n')

print('compiling model...')
model.compile(optimizer=OPTIMIZER, metrics=['accuracy'], loss=LOSS_FUNCTION)
print('done \n')

print('fitting model... ')
history = model.fit_generator(train_generator, epochs=EPOCH, verbose=1, validation_data=validation_generator)
print('done \n')

print('evaluating model... ')
y_actual = test_generator.classes
y_predicted = model.predict_generator(test_generator)
test_result = model.evaluate_generator(test_generator)
print("done \n")

print("Test loss and accuracy: ", test_result, "\n")


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
    logging.info(get_confusion_matrix(y_actual=y_actual, y_predicted=y_predicted))

if PLOT_TRAINING_HISTORY:
    plot_acc_history(history)
    plot_loss_history(history)
