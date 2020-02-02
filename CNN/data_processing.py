import cv2
import numpy as np
from face_detection import getxywh


def crop_face_single(pixel_array, resize=True):
    if pixel_array.ndim == 3:
        y, x, channel = pixel_array.shape
    else:
        y, x = pixel_array.shape

    if pixel_array.ndim == 2:
        pixel_original = pixel_array
        pixel_array = np.stack((pixel_array,) * 3, axis=-1)
    from face_detection import detect_faces
    faces = detect_faces(pixel_array)

    if pixel_array.ndim == 2:
        pixel_array = pixel_original

    if len(faces) != 1:
        return pixel_array
    box_x, box_y, box_w, box_h = getxywh(faces[0])

    y_start = box_y
    y_end = box_y + box_h
    x_start = box_x
    x_end = box_x + box_w
    if y_start < 0:
        y_start = 0
    if x_start < 0:
        x_start = 0
    if y_end > y-1:
        y_end = y-1
    if x_end > y-1:
        x_end = y-1
    crop_img = pixel_array[y_start:y_end, x_start:x_end]

    if resize:
        return cv2.resize(crop_img, (x, y))
    else:
        return crop_img


def process_face(image, face, size):
    box_x, box_y, box_w, box_h = getxywh(face)
    image = image[box_y:box_y + box_h, box_x:box_x + box_w]
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image = cv2.resize(image, size)
    image = np.true_divide(image, 255)
    image = np.stack((image,) * 3, axis=-1)
    return image
