This is the final project of Master of Information Technology of University of Melbourne.

This is the Android application of Human emotion through deep learning. 

![State diagram](https://github.com/nnyy10/COMP90055_CNN_Emotion_Recognition/blob/master/Android/image/app_state.png)

Open the applications, users can directly use the main functions of this project. There are three models for users to choose, inception-resnet, mobilenetv2 and yolo3. Users can choose a photo from gallery or take a picture, then upload the image. The processed image and detailed results wil be shown. In the image, a bounding box is drawn on each face in the photo along with their predictions. For yolo3 model, it returns an emotion which has the highest emotion score, while other models return seven emotions which are sorted by emotion probabilities from high to low. 

If users want to use more functions, they need to log in. If users have no account, they need to sign up with email and password. There are four main pages after loging in, home, uplaod, history and profile. There are some introductions in the home page. In the upload page, functions are the same as before. The difference is that this upload function will save data to database and the results will show in the history page. Next, in the history page, users can see a history of all previous predictions. Such as submit time, image name, processed image and predict results. In the profile page, it shows account information. Finally, users can log out the account and back to the login page. 

![Data transmission](https://github.com/nnyy10/COMP90055_CNN_Emotion_Recognition/blob/master/Android/image/IMG_6016.JPG)

When uploading images, the android application is sending a HTTP post to web server, using predict rest API and acquiring a json result. After signing in, the related data of users will be stored to firebase. There are three sections of firebase. Authentication stores information of accounts. Realtime database stores all previous predictions, and storage has upload images and each cropped face image. 
