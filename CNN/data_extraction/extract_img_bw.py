import os
import cv2
import numpy as np


def num_to_expression(number):
    if number == 0:
        return "Neutral"
    elif number == 1:
        return "Happy"
    elif number == 2:
        return "Sad"
    elif number == 3:
        return "Surprise"
    elif number == 4:
        return "Fear"
    elif number == 5:
        return "Disgust"
    elif number == 6:
        return "Anger"
    elif number == 7:
        return "Contempt"
    elif number == 8:
        return "None"
    elif number == 9:
        return "Uncertain"
    elif number == 10:
        return "No-face"

counter = np.zeros(11)

#neutral, happy, sad, surprise, fear, disgust, anger, contempt, none, uncertain, noface
counter_train = np.zeros(11)
counter_validation = np.zeros(11)
counter_test = np.zeros(11)

cnt = 0

path = "C:\\Users\\naiyu\\Documents\\Naiyun\\ProcessedData\\colored\\train"
save_path = "C:\\Users\\naiyu\\Documents\\Naiyun\\ProcessedData\\blackwhite\\train"

emotions = list(os.listdir("C:\\Users\\naiyu\\Documents\\Naiyun\\ProcessedData\\colored\\train"))

counter = 0

for emotion in emotions:
    image_names = os.listdir(os.path.join("C:\\Users\\naiyu\\Documents\\Naiyun\\ProcessedData\\colored\\train\\", emotion))
    save_emotion_path = os.path.join(save_path,emotion)
    for image_name in image_names:
        image_dir = os.path.join(path, emotion, image_name)
        img = cv2.imread(image_dir, cv2.IMREAD_GRAYSCALE)

        save_image_path = os.path.join(save_emotion_path, image_name)
        cv2.imwrite(save_image_path, img)

        counter += 1
        print(counter)

        # read image as bw
        # save image in new dir as bw