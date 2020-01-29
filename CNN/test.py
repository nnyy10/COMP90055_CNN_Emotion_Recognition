from utils import *
import os
import pycm

base_image_path = 'data/processed_data'
image_type_path = 'base'
x_test_new = []
x_test = np.load(os.path.join(base_image_path, image_type_path, 'x_test.npy'))
x_test = np.true_divide(x_test, 255)
y_test = np.load(os.path.join(base_image_path, image_type_path, 'y_test.npy'))

print('loading model...')
model = load_model('mode_v1.h5')
print('done \n')

def hello():

    print('making predictions...')
    predictions = model.predict(x_test)
    print('done \n')
    print(print_confusion_matrix(predictions, y_test))

import keyboard  # using module keyboard
import time
while True:  # making a loop
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('q'):  # if key 'q' is pressed
            print('Start')
            hello()
            print("end \n")
            time.sleep(0.1)

    except:
        break  # if user pressed a key other than the given key the loop will break