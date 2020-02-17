import os

import tensorflow as tf
from keras_preprocessing.image import ImageDataGenerator

from utils import get_confusion_matrix
DATA_SET_LIST = ["blackwhite_original", "blackwhite_reduced", "colored_original", "colored_reduced"]
DATA_SET_NAME = DATA_SET_LIST[0]
IMG_SIZE = (160, 160)
BATCH_SIZE = 64

model = tf.keras.models.load_model("model/keras/model/DAblackwhite_original_BS64_EP12_OPAdam_LOcategorical_crossentropy_MOpretrained_facenet_inception_v1_TRA77_TEA53_WA.h5")

test_datagen = ImageDataGenerator(rescale=1. / 255)
DATA_DIR = "C:\\Users\\naiyu\\Documents\\Naiyun\\ProcessedData"
TEST_DIR = os.path.join(DATA_DIR, DATA_SET_NAME, "test")

test_generator = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE, shuffle=False)

y_actual = test_generator.classes
y_predicted = model.predict_generator(test_generator)

print(get_confusion_matrix(y_actual=y_actual, y_predicted=y_predicted))