# -*- coding: utf-8 -*-
"""
Python scripts to test ensembling of 3 different trained models.
"""

import keras
import numpy as np
from keras_preprocessing.image import ImageDataGenerator
from utils import get_confusion_matrix

model1 = keras.models.load_model("C:\\Users\\naiyu\\OneDrive\\Skrivebord\\COMP90055_CNN_Emotion_Recognition\\CNN\log\\5. Ensemble\\old_1.h5")
model2 = keras.models.load_model("C:\\Users\\naiyu\\OneDrive\\Skrivebord\\COMP90055_CNN_Emotion_Recognition\\CNN\log\\5. Ensemble\\new_1.h5")
model3 = keras.models.load_model("C:\\Users\\naiyu\\OneDrive\\Skrivebord\\COMP90055_CNN_Emotion_Recognition\\CNN\log\\5. Ensemble\\new_2.h5")
data_directory = "data/processed_data/cropped"

def preprocess(nparr):
    result = np.subtract(nparr, 0.5077424916139078)
    result = np.true_divide(result, 0.25016892401139035)
    return result
test_datagen = ImageDataGenerator(rescale=1. / 255,
                                  featurewise_center=True,
                                  featurewise_std_normalization=True,
                                  preprocessing_function=preprocess)

test_generator = test_datagen.flow_from_directory(
    "data/processed_data/cropped_img/test",
    target_size=(160,160),
    batch_size=64, shuffle=False)
label_map = (test_generator.class_indices)
print(label_map)
test_result1 = model1.evaluate_generator(test_generator)
test_result2 = model2.evaluate_generator(test_generator)
test_result3 = model3.evaluate_generator(test_generator)
print(test_result1)
print(test_result2)
print(test_result3)

y_predicted1 = model1.predict_generator(test_generator)
y_predicted2 = model2.predict_generator(test_generator)
y_predicted3 = model3.predict_generator(test_generator)
y_actual = test_generator.classes

prediction = np.true_divide(np.add(np.add(y_predicted1, y_predicted2), y_predicted3), 3)
print(get_confusion_matrix(y_actual=y_actual, y_predicted=prediction))
