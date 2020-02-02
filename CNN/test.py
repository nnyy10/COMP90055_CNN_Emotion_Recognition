import cv2


image_path = 'data/images/gettyimages-514325215-612x612.jpg'
image = cv2.imread(image_path)
print(image.shape)