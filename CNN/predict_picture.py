from utils import *


print('Reading image...')
image_path = 'data/images/gettyimages-514325215-612x612.jpg'
image = cv2.imread(image_path)
print('done \n')

print('detecting faces...')
faces = detect_faces(image)
print('done \n')

if len(faces) == 0:
    print("no face detected in image")
    exit(0)

# optional line to see the faces in the image
display_all_faces(image, faces)

print('processing faces...')
processed_faces = [process_face(image, face) for face in faces]
processed_faces = np.array(processed_faces)
print('done \n')

print('loading model...')
model = load_model('mode_v1.h5')
print('done \n')

print('making predictions...')
predictions = model.predict(processed_faces)
print('done \n')

print(predictions)
print('the predicted emotion is: ', get_predicted_emotion(predictions[0]))
