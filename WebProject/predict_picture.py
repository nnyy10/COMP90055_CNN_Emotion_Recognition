from utils import *
import cv2
from keras import backend as K

# model = None
#
# def load_model_first_time():
#     global model
#     model = load_model('best_model.h5')
#     global graph
#     graph = tf.get_default_graph()
#
#
# load_model_first_time()


def predict(image):
    print('detecting faces...')
    faces = detect_faces(image)
    print('done \n')

    if len(faces) == 0:
        print("no face detected in image")
        return None

    # optional line to see the faces in the image
    # display_all_faces(image, faces)

    print('processing faces...')
    processed_faces = [process_face(image, face) for face in faces]
    processed_faces = np.array(processed_faces)
    print('done \n')

    # with graph.as_default():
    print('making predictions...')
    model = load_model('model/best_model.h5')
    predictions = model.predict(processed_faces)
    K.clear_session()
    print('done \n')

    print(predictions)
    emotion = get_predicted_emotion(predictions[0])
    print('the predicted emotion is: ', emotion)

    return emotion
