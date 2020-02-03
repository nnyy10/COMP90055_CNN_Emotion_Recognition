import numpy as np
import tensorflow as tf
import keras
from os import path
from utils import load_data_from_npy, y_single_to_list, plot_loss_history, plot_acc_history, print_confusion_matrix
from data_processing import format_x
from models import *


BATCH_SIZE = 64
EPOCH = 4
OPTIMIZER = keras.optimizers.RMSprop(lr=0.00001)
LOSS_FUNCTION = tf.keras.losses.categorical_crossentropy
SAVE_MODEL = True
PLOT_TRAINING_HISTORY = False
PRINT_CONFUSION_MATRIX = True

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
print('model_compiled')

print('fitting model... ')
history = model.fit(x_train, y_train, batch_size=BATCH_SIZE, epochs=EPOCH, verbose=1, validation_data=(x_valid, y_valid))
print('done \n')

test_result = model.evaluate(x_test, y_test)
print("\nTest loss and accuracy: ", test_result)

if SAVE_MODEL:
    save_model_dir = "model/keras/model/"
    train_result = model.evaluate(x_train, y_train)
    SAVE_MODEL_NAME = "DA{0}_BS{1}_EP{2}_OP{3}_LO{4}_MO{5}_TRA{6}_TEA{7}{8}.h5".format(DATA_SET_NAME,
                                                                                       str(int(BATCH_SIZE)),
                                                                                       str(int(EPOCH)),
                                                                                       OPTIMIZER.__class__.__name__,
                                                                                       LOSS_FUNCTION.__name__,
                                                                                       model_initializer.__name__,
                                                                                       str(int(train_result[1] * 100)),
                                                                                       str(int(test_result[1] * 100)),
                                                                                       MODEL_NAME_ID)
    model.save(path.join(save_model_dir, SAVE_MODEL_NAME))

if PLOT_TRAINING_HISTORY:
    plot_acc_history(history)
    plot_loss_history(history)

if PRINT_CONFUSION_MATRIX:
    y_predicted = model.predict(x_test)
    print_confusion_matrix(y_actual=y_test, y_predicted=y_predicted)
