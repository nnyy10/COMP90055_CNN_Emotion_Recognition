import csv
import os
import numpy as np
import shutil
import ntpath


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

def process_csv_file(file_path):

    with open(file_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        readCSV.__next__()



        # counter_train = [68885,123663,23423,12964,5868,3499,22892,3450,30442,10715,75823]
        # counter_validation = [2995, 5376, 1018, 563, 255, 152, 995, 150, 1323, 465, 3296]
        # counter_test = [2994, 5376, 1018, 563, 255, 152, 995, 150, 1323, 465, 3296]

        for row in readCSV:
            expression_int = int(row[6])
            expression = num_to_expression(expression_int)

            img_path = row[0]
            img_path = os.path.join(base_img_path, img_path)
            img_name = ntpath.basename(img_path)
            img_name_raw, img_extension = os.path.splitext(img_path)

            if counter[expression_int] % 8 == 7 and counter_validation[expression_int] < 500:
                save_img_path = "validation"
                num_to_append = counter_validation[expression_int]
                counter_validation[expression_int] += 1
            elif counter[expression_int] % 8 == 6 and counter_test[expression_int] < 500:
                save_img_path = "test"
                num_to_append = counter_test[expression_int]
                counter_test[expression_int] += 1
            else:
                save_img_path = "train"
                num_to_append = counter_train[expression_int]
                counter_train[expression_int] += 1


            destination_path = os.path.join(save_base_img_path, save_img_path)
            destination_path = os.path.join(destination_path, expression)

            new_destination_file_name = os.path.join(destination_path, expression + "_" + str(int(num_to_append)) + img_extension)

            shutil.move(img_path, new_destination_file_name)


            counter[expression_int] += 1
            global cnt
            cnt += 1
            print(cnt)

base_img_path = "C:\\Users\\naiyu\\Documents\\Naiyun\\Manually_Annotated\\Manually_Annotated_Images"
save_base_img_path = "C:\\Users\\naiyu\\Documents\\Naiyun\\ProcessedData"
train_file_list_path = "C:\\Users\\naiyu\\Documents\\Naiyun\\Manually_Annotated_file_lists\\training.csv"
validation_file_list_path = "C:\\Users\\naiyu\\Documents\\Naiyun\\Manually_Annotated_file_lists\\validation.csv"

process_csv_file(train_file_list_path)
process_csv_file(validation_file_list_path)






# import tensorflow as tf
#
# mnist = tf.keras.datasets.mnist
#
# (x_train, y_train), (x_test, y_test) = mnist.load_data()
#
#
#
# x_train = tf.keras.utils.normalize(x_train, axis=1)
# x_test = tf.keras.utils.normalize(x_test, axis=1)
#
# new_model = tf.keras.models.load_model('bestmodel.model')
#
#
# val_loss, val_accuracy = new_model.evaluate(x_test, y_test)
# print(val_loss, val_accuracy)
#
# predictions = new_model.predict([[x_test[0]]])
#
# import numpy as np
# print(np.argmax(predictions))
#
# import matplotlib.pyplot as plt
# plt.imshow(x_test[0], cmap=plt.cm.binary)
# plt.show()

