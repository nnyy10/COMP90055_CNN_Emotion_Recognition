import csv
import os
import cv2
from face_detection import detect_faces, getxywh
import numpy as np


base_dir = "C:\\Users\\naiyu\\Documents\\Naiyun"
csv_dir = "Manually_Annotated_file_lists\\training.csv"

csv_path = os.path.join(base_dir, csv_dir)
# subDirectory_filePath	face_x	face_y	face_width	face_height	facial_landmarks	expression	valence	arousal

base_save_path = "/data/NiuTong"

emotion_counter = np.zeros(11)

File_object = open(r"../output.txt", "w")
counter = 0

with open(csv_path, "r") as f:
    reader = csv.reader(f, delimiter=",")
    reader.__next__()
    for line in reader:
        image_path = os.path.join(base_dir, "Manually_Annotated", "Manually_Annotated_Images", line[0].replace("/","\\"))
        emotion = int(line[6])
        if emotion_counter[emotion] > 499:
            stop_cond = True
            for e in emotion_counter:
                if e < 500:
                    stop_cond = False
                    break
            if stop_cond:
                break
            continue

        img = cv2.imread(image_path)
        img = cv2.resize(img, (416, 416))
        faces = detect_faces(img)
        if len(faces) != 1:
            face_x_start = 0
            face_y_start = 0
            face_x_end = 415
            face_y_end = 415
        else:
            x, y, w, h = getxywh(faces[0])
            face_x_start = x
            face_y_start = y
            face_x_end = face_x_start + w
            face_y_end = face_y_start + h

            if face_x_start < 0:
                face_x_start = 0
            if face_y_start < 0:
                face_y_start = 0
            if face_x_end > 415:
                face_x_end = 415
            if face_y_end > 415:
                face_y_end = 415

        save_img_name = str(emotion) + "_" + str(int(emotion_counter[emotion])) + ".jpg"
        emotion_counter[emotion] += 1

        write_log_path = os.path.join("../data", "train", str(emotion), save_img_name)
        save_img_path = os.path.join(base_save_path, str(emotion), save_img_name)
        cv2.imwrite(save_img_path, img)

        log_line = write_log_path + " " + str(face_x_start) + "," + str(face_y_start) + "," + \
                       str(face_x_end) + "," + str(face_y_end) + "," + str(emotion) + "\n"

        File_object.write(log_line)
        print(log_line)
        counter += 1
        print(counter)
