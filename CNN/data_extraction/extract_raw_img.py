import csv
import numpy as np
from data_processing import *
from PIL import Image
import os


DATA_DIR = "../data/icml_face_data.csv"
SAVE_DIR_BASE = "../data/processed_data/raw_img"

TRAIN_LABEL = "Training"
PUB_TEST_LABEL = "PublicTest"
PRI_TEST_LABEL = "PrivateTest"

train_tot_counter = 0
train_emotion_counter = np.zeros(7)
pub_test_tot_counter = 0
pub_test_emotion_counter = np.zeros(7)
pri_test_tot_counter = 0
pri_test_emotion_counter = np.zeros(7)

x_train = []
x_test = []
x_valid = []
y_train = []
y_test = []
y_valid = []

counter = 0
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
            directory = "train"
            img_name = emotion_str + "_" + str(int(train_emotion_counter[emotion_int])) + ".jpg"
            train_tot_counter += 1
            train_emotion_counter[emotion_int] += 1
        elif purpose == PUB_TEST_LABEL:
            directory = "test"
            img_name = emotion_str + "_" + str(int(pub_test_emotion_counter[emotion_int])) + ".jpg"
            pub_test_tot_counter += 1
            pub_test_emotion_counter[emotion_int] += 1
        elif purpose == PRI_TEST_LABEL:
            directory = "valid"
            img_name = emotion_str + "_" + str(int(pri_test_emotion_counter[emotion_int])) + ".jpg"
            pri_test_tot_counter += 1
            pri_test_emotion_counter[emotion_int] += 1

        save_path = os.path.join(SAVE_DIR_BASE, directory, emotion_str, img_name)
        image = Image.fromarray(pixel_array)
        image.save(save_path)

        counter += 1
        print(counter)