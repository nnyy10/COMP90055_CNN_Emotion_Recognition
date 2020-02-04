import numpy as np
import tensorflow as tf
import keras
from os import path
from utils import load_data_from_npy, y_single_to_list, plot_loss_history, plot_acc_history, print_confusion_matrix
from data_processing import format_x
from models import *
from keras.preprocessing.image import ImageDataGenerator

BATCH_SIZE = 64
EPOCH = 30
OPTIMIZER = keras.optimizers.RMSprop(lr=0.00001)
LOSS_FUNCTION = tf.keras.losses.categorical_crossentropy
SAVE_MODEL = True
PLOT_TRAINING_HISTORY = False
PRINT_CONFUSION_MATRIX = True

model_initializer = pretrained_facenet_inception_v1
model = model_initializer(print_summary=False)

# ka = kaggle, uc = uncropped
DATA_SET_NAME = "KAC"
# if you wish to give the model an ID
MODEL_NAME_ID = ""

print('creating data generator')
train_datagen = ImageDataGenerator(rescale=1. / 255,
                                   rotation_range=45,
                                   width_shift_range=0.2,
                                   height_shift_range=0.2,
                                   brightness_range=[0.7, 1.3],
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1. / 255)

TRAIN_DIR = "data/processed_data/cropped_img/train"
VALID_DIR = "data/processed_data/cropped_img/valid"
TEST_DIR = "data/processed_data/cropped_img/test"
train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(160, 160),
    batch_size=64)

validation_generator = test_datagen.flow_from_directory(
    VALID_DIR,
    target_size=(160, 160),
    batch_size=64)

test_generator = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=(160, 160),
    batch_size=64)
print('done \n')

print('compiling model...')
model.compile(optimizer=OPTIMIZER, metrics=['accuracy'], loss=LOSS_FUNCTION)
print('done \n')

print('fitting model... ')

history = model.fit_generator(train_generator, epochs=EPOCH, verbose=1, validation_data=validation_generator)
print('done \n')

test_result = model.evaluate_generator(test_generator)
print("\nTest loss and accuracy: ", test_result)

if SAVE_MODEL:
    save_model_dir = "model/keras/model/"
    train_result = model.evaluate(train_generator)
    SAVE_MODEL_NAME = "DA{0}_BS{1}_EP{2}_OP{3}_LO{4}_MO{5}_TRA{6}_TEA{7}{8}_WA.h5".format(DATA_SET_NAME,
                                                                                          str(int(BATCH_SIZE)),
                                                                                          str(int(EPOCH)),
                                                                                          OPTIMIZER.__class__.__name__,
                                                                                          LOSS_FUNCTION.__name__,
                                                                                          model_initializer.__name__,
                                                                                          str(int(
                                                                                              train_result[1] * 100)),
                                                                                          str(int(
                                                                                              test_result[1] * 100)),
                                                                                          MODEL_NAME_ID)
    model.save(path.join(save_model_dir, SAVE_MODEL_NAME))

if PLOT_TRAINING_HISTORY:
    plot_acc_history(history)
    plot_loss_history(history)

if PRINT_CONFUSION_MATRIX:
    pass
    # y_predicted = model.predict_generator(test_generator)
    # print_confusion_matrix(y_actual=y_test, y_predicted=y_predicted)
