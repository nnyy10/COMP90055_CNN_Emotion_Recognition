# ----------------------------------------------------------------------------
"""Import modules"""
import numpy as np
import tensorflow as tf
import keras
from os import path
from utils import plot_loss_history, plot_acc_history, get_confusion_matrix
from models import *
from keras.preprocessing.image import ImageDataGenerator
import logging
import os
from collections import Counter
from sklearn.utils import class_weight


# ----------------------------------------------------------------------------
"""Set training parameters"""
BATCH_SIZE = 64
EPOCH = 50
OPTIMIZER = keras.optimizers.RMSprop(lr=0.00001)
# OPTIMIZER = "adadelta"
LOSS_FUNCTION = tf.keras.losses.categorical_crossentropy
# LOSS_FUNCTION = tf.keras.losses.squared_hinge
SAVE_MODEL = True
LOG = True
PLOT_TRAINING_HISTORY = False
# # CLASS_WEIGHT = {0:}
y = np.concatenate((np.zeros(74374),
                   np.ones(133915),
                   np.ones(24959)*2,
                   np.ones(13590)*3,
                   np.ones(5878)*4,
                   np.ones(3303)*5,
                   np.ones(24382)*6))


class_weights = class_weight.compute_class_weight('balanced', np.array([0, 1, 2, 3, 4, 5, 6]), y)
# class_weights_dict = {}
# for i in range(7):
#     class_weights_dict[i] = class_weights[i]

print(class_weights)

print("loading model...")
model_initializer = pretrained_facenet_inception_v1
model = model_initializer(print_summary=True)
print("done \n")

# ka = kaggle, uc = uncropped
# DATA_SET_LIST = ["blackwhite_original", "blackwhite_reduced", "colored_original", "colored_reduced"]
# DATA_SET_NAME = DATA_SET_LIST[0]
DATA_SET_NAME = "kac"
# if you wish to give the model an ID
MODEL_NAME_ID = "valot3"

IMG_SIZE = (160, 160)


# ----------------------------------------------------------------------------
"""Load data"""
print('creating data generator')
train_datagen = ImageDataGenerator(rescale=1. / 255,
                                   rotation_range=45,
                                   width_shift_range=0.2,
                                   height_shift_range=0.2,
                                   brightness_range=[0.5, 1.5],
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True)
# train_datagen = ImageDataGenerator(rescale=1. / 255)

test_datagen = ImageDataGenerator(rescale=1. / 255)

TRAIN_DIR = "data/processed_data/cropped_img/train"
VALID_DIR = "data/processed_data/cropped_img/valid"
TEST_DIR = "data/processed_data/cropped_img/test"
# DATA_DIR = "C:\\Users\\naiyu\\Documents\\Naiyun\\ProcessedData"
# TRAIN_DIR = os.path.join(DATA_DIR, DATA_SET_NAME, "train")
# VALID_DIR = os.path.join(DATA_DIR, DATA_SET_NAME, "valid")
# TEST_DIR = os.path.join(DATA_DIR, DATA_SET_NAME, "test")

train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE)

validation_generator = test_datagen.flow_from_directory(
    VALID_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE)

test_generator = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE, shuffle=False)
print('done \n')

print('compiling model...')
model.compile(optimizer=OPTIMIZER, metrics=['accuracy'], loss=LOSS_FUNCTION)
print('done \n')

print('fitting model... ')
# history = model.fit_generator(train_generator, epochs=EPOCH, verbose=1, validation_data=validation_generator, class_weight=class_weights)
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
