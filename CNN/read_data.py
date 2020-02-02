import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import scipy
import mtcnn
import utils
import cv2

DATA_DIR = "data/icml_face_data.csv"

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

detector = None


def process_picture(picture):
    pixel_array = picture.split(' ')
    pixel_array = np.array(list(map(int, pixel_array)), dtype=np.uint8)
    pixel_array = np.reshape(pixel_array, (-1, 48))
    pixel_array = np.stack((pixel_array,) * 3, axis=-1)
    global detector
    if detector is None:
        detector = mtcnn.MTCNN()

    faces = [face["box"] for face in detector.detect_faces(pixel_array)]
    if len(faces) != 1:
        return pixel_array
    box_x, box_y, box_w, box_h = utils.getxywh(faces[0])

    y_start = box_y
    y_end = box_y + box_h
    x_start = box_x
    x_end = box_x + box_w
    if y_start < 0:
        y_start = 0
    if x_start < 0:
        x_start = 0
    if y_end > 47:
        y_end = 47
    if x_end > 47:
        x_end = 47
    crop_img = pixel_array[y_start:y_end, x_start:x_end]

    resized = cv2.resize(crop_img, (48, 48))
    return resized

counter = 0
counter_none = 0
with open(DATA_DIR, "r") as f:
    reader = csv.reader(f, delimiter=",")
    reader.__next__()
    for line in reader:
        emotion = int(line[0])
        purpose = line[1]
        picture = process_picture(line[2])

        counter += 1
        print(counter, " : ", counter_none)
        if purpose == TRAIN_LABEL:
            train_tot_counter += 1
            train_emotion_counter[emotion] = train_emotion_counter[emotion] + 1
            x_train.append(picture)
            y_train.append(emotion)
        elif purpose == PUB_TEST_LABEL:
            pub_test_tot_counter += 1
            pub_test_emotion_counter[emotion] += 1
            x_test.append(picture)
            y_test.append(emotion)
        elif purpose == PRI_TEST_LABEL:
            pri_test_tot_counter += 1
            pri_test_emotion_counter[emotion] += 1
            x_valid.append(picture)
            y_valid.append(emotion)

def process_y(y_list):
    new_y_list = []
    for y in y_list:
        new_y = np.zeros(7)
        new_y[y] = 1
        new_y_list.append(new_y)
    return np.asarray(new_y_list)

print('reformatting data...')
x_train = np.asarray(x_train)
x_test = np.asarray(x_test)
x_valid = np.asarray(x_valid)
y_train = process_y(y_train)
y_test = process_y(y_test)
y_valid = process_y(y_valid)
print('done \n ')

np.save('data/processed_data/cropped/x_train.npy', x_train)
np.save('data/processed_data/cropped/x_test.npy', x_test)
np.save('data/processed_data/cropped/x_valid.npy', x_valid)
np.save('y_train', y_train)
np.save('y_test', y_test)
np.save('y_valid', y_valid)

# print(train_emotion_counter)
# print(pub_test_emotion_counter)
#
# print(train_tot_counter)
# print(pub_test_tot_counter)
#
# N = 7
#
# ind = np.arange(N)  # the x locations for the groups
# width = 0.35       # the width of the bars
#
# fig = plt.figure()
# ax = fig.add_subplot(111)
# rects1 = ax.bar(ind, pub_test_emotion_counter, width, color='royalblue')
# rects2 = ax.bar(ind+width, train_emotion_counter, width, color='seagreen')
#
# # add some
# ax.set_ylabel('Scores')
# ax.set_title('Scores by group and gender')
# ax.set_xticks(ind + width / 2)
# ax.set_xticklabels( ('0','1', '2', '3', '4', '5','6') )
#
# ax.legend( (rects1[0], rects2[0]), ('test', 'train') )
#
# plt.show()
#
#
#
# x_test_embedded = TSNE(n_components=2).fit_transform(x_test)
#
# print(x_test_embedded)