# CNN

This "CNN" folder contains the data extraction scripts, data processing scripts and model training scripts of Inception-resnet and mobilenet v2

## Transfer learning - pre-trained models

Since we are using transfer learning, the first step was to find pretrained Inception-resnet and mobilenetv2 models to use. Both had pretrained models in keras.applications (https://keras.io/applications/) on imagenet. However, for inception-resnet, we found a pre-trained model by David Sandberg (https://github.com/davidsandberg/facenet) trained on 3 million human faces acheiving and accuracy of 0.9965 accuracy on LFW face detection competition which most likely had better trained filters/features for human face detection/emotion recognition. However, the model was saved as tensorflow v1 model and we wanted to use tensorflow v2 for some functionalities such as data augmentation. Another github author provided scripts to convert the models trained by David Sandberg to h5 model (https://github.com/nyoki-mtl/keras-facenet). This script is saved in the model_conversion folder and this script requires tensorflow 1.15.2 to run.

The steps to run this conversion script is:
1. Download the tensorflow v1 model by David Sandberg to model/tf/.
2. Change the `tf_model_dir` in the script accordingly.
3. Run this script which will generate model/keras/model/facenet_keras.h5 which is the converted model to tensorflow v2
4. Load facenet_keras.h5 to use for transfer learning.

For mobilenetv2, we simply used keras.applications's pretrained model on imagenet.

## Data processing and extraction

For inception-resnet and mobilenetv2, we used a dataset provided by kaggle (details can be found https://www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge/overview). This dataset contains ~36,000 black and white 48x48 images of human faces already cropped and labeled. The labeled data include ~29,000 train data and ~3,500 test data and ~3,500 validation data. The data is imbalanced having 13.91% Angry, 1.51% Disgust, 14.27% Fear, 25.13% Happy, 16.82% Sad, 11.04% Surprised, 17.29% Neutral.

The data comes in a single CSV file with 1 column being the pixel array values, another column indicating the emotion.
There are 4 data extraction scripts written for this data:

**extract_raw_img.py** - converts the image array in csv to a jpg and save it in data/processed_data/raw_img. The saved images will be sorted to train, test or validation data and sorted in to their respective class folders. This structure is nessesary for keras to read in the data.

**extract_raw_img_data.py** - converts the image array in csv to a jpg and save it in data/processed_data/raw as .npy file format for easy loading with Numpy if nessesary

**extract_cropped_img.py** - reads the image array in, uses MTCNN to crop the image, resize the cropped image back to 48x48 and saves it to a jpg and save it in data/processed_data/cropped_img.

**extract_cropped_img_data.py** - reads the image array in, uses MTCNN to crop the image, resize the cropped image back to 48x48 and saves it as .npy file for numpy loading if nessesary.

The other files in data_extraction is used for training in YOLO and is not relavent for this CNN project with inception-resnet and mobilenetv2.

## Model training and fine tuning

All models used are created in the "models.py" file

There are 2 training files: train_batches.py and train_whole.py. train_whole.py loads the data from npy while train_batches.py loads the data from the jpgs extracted from the previous scripts.
There are variables such as batch size, image size, epoch, loss function at the top of these two files which can be changed easily.
If the LOG variable is set to true, it will log all hyperparameters to the CNN/log/ folder along with training, validation loss and accuracy as well as a confusion matrix.


data_processing.py, utils.py and face_detection.py contains helper functions for training and data extraction.

predict_picture.py reads a single image and makes predictions, a similar file exists in WebProject/app.

predict_ensemble reads in 3 files, takes an average of the predictions and outputs a final prediction. This file was used to test the method of enembling of three different models to see whether the accuracy would increase or not.

