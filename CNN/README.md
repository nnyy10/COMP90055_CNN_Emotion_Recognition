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

For inception-resnet and mobilenetv2, we used a dataset provided by kaggle (details can be found https://www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge/overview)
