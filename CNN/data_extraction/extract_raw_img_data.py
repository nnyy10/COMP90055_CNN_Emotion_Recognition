# -*- coding: utf-8 -*-
"""
This module converts the image array in csv to a jpg and save it in data/processed_data/raw as .npy file format for easy
loading with Numpy if necessary.
"""
import csv
import numpy as np
from utils import emotion_int_to_str

DATA_DIR = "../data/icml_face_data.csv"

TRAIN_LABEL = "Training"
PUB_TEST_LABEL = "PublicTest"
PRI_TEST_LABEL = "PrivateTest"

x_train = []
x_test = []
x_valid = []
y_train = []
y_test = []
y_valid = []


with open(DATA_DIR, "r") as f:
    reader = csv.reader(f, delimiter=",")
    reader.__next__()
    for line in reader:
        emotion_int = int(line[0])
        emotion_str = emotion_int_to_str(emotion_int)
        purpose = line[1]
        pixel_array = line[2].split(' ')
        pixel_array = np.array(list(map(int, pixel_array)), dtype=np.uint8)
        pixel_array = np.reshape(pixel_array, (-1, 48))

        if purpose == TRAIN_LABEL:
            x_train.append(pixel_array)
            y_train.append(emotion_int)
        elif purpose == PUB_TEST_LABEL:
            x_test.append(pixel_array)
            y_test.append(emotion_int)
        elif purpose == PRI_TEST_LABEL:
            x_valid.append(pixel_array)
            y_valid.append(emotion_int)

x_train = np.asarray(x_train)
x_test = np.asarray(x_test)
x_valid = np.asarray(x_valid)
y_train = np.asarray(y_train)
y_test = np.asarray(y_test)
y_valid = np.asarray(y_valid)

np.save('../data/processed_data/raw/x_train.npy', x_train)
np.save('../data/processed_data/raw/x_test.npy', x_test)
np.save('../data/processed_data/raw/x_valid.npy', x_valid)
np.save('../data/processed_data/raw/y_train.npy', y_train)
np.save('../data/processed_data/raw/y_test.npy', y_test)
np.save('../data/processed_data/raw/y_valid.npy', y_valid)