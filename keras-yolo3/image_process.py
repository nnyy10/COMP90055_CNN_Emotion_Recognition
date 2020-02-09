import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb
from mtcnn import MTCNN
import random
import csv
import os


def pad_image(image, target_size):
    iw, ih = image.size  # 原始图像的尺寸
    w, h = target_size  # 目标图像的尺寸
    print(iw, ih, target_size)
    scale = min(float(w) / float(iw), float(h) / float(ih))  # 转换的最小比例

    # 保证长或宽，至少一个符合目标图像的尺寸
    nw = int(iw * scale)
    nh = int(ih * scale)
    image = image.resize((nw, nh), Image.BICUBIC)  # 缩小图像
    # image.show()

    new_image = Image.new('RGB', (w,h), (128, 128, 128))  # 生成灰色图像
    # // 为整数除法，计算图像的位置
    new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))  # 将图像填充为中间图像，两侧为灰色的样式
    #new_image.paste(image, (30,0))


    # new_image.show()

    return new_image

def cut_box(num_box,orig_size):
    if num_box in [1,2,4,9]:
        orig_w,orig_h= orig_size
        box_size=[]
        if num_box == 1:
            box_size.append(orig_size)
            one_loc =[(0,0)]
            box_size.append(one_loc)
        if num_box == 2:
            cut_line = random.randint(60,356)
            box_size.append([cut_line,orig_h])
            box_size.append([orig_w-cut_line,orig_h])
            two_loc = [(0,0),(cut_line,0)]
            box_size.append(two_loc)
        if num_box == 4:
            cutw_line = random.randint(60,356)
            cuth_line = random.randint(60, 356)
            box_size.append([cutw_line,cuth_line])
            box_size.append([orig_w-cutw_line,cuth_line])
            box_size.append([cutw_line,orig_h-cuth_line])
            box_size.append([orig_w-cutw_line,orig_h-cuth_line])
            four_loc = [(0,0),(cutw_line,0),(0,cuth_line),(cutw_line,cuth_line)]
            box_size.append(four_loc)
        if num_box ==9:
            cutw_line1 = random.randint(60, 178)
            cutw_line2 = random.randint(239, 356)
            cuth_line1 = random.randint(60, 178)
            cuth_line2 = random.randint(239, 356)
            '''
            -------w1------w2----------
            |      |       |           |
            h1-----|-------|-----------|          
            |      |       |           |
            |      |       |           |
            h2-----|-------|-----------|
            |      |       |           |
            ---------------------------
            '''
            box_size.append([cutw_line1, cuth_line1])
            box_size.append([cutw_line2-cutw_line1, cuth_line1])
            box_size.append([orig_w-cutw_line2, cuth_line1])
            box_size.append([cutw_line1, cuth_line2-cuth_line1])
            box_size.append([cutw_line2 - cutw_line1, cuth_line2-cuth_line1])
            box_size.append([orig_w - cutw_line2, cuth_line2-cuth_line1])
            box_size.append([cutw_line1, orig_h - cuth_line2])
            box_size.append([cutw_line2 - cutw_line1, orig_h - cuth_line2])
            box_size.append([orig_w - cutw_line2, orig_h - cuth_line2])
            nine_loc = [(0,0),(cutw_line1,0),(cutw_line2,0),
                        (0,cuth_line1),(cutw_line1,cuth_line1),(cutw_line2,cuth_line1),
                        (0,cuth_line2),(cutw_line1,cuth_line2),(cutw_line2,cuth_line2)]
            box_size.append(nine_loc)
        return box_size
    else:
        print("Number of boxes should be in (1,2,4,9)")

def img_fill(num_box,images_set):
    target_size = [416,416]
    boxes_size = cut_box(num_box,target_size)
    if num_box == len(boxes_size)-1:
        # randomly return same numbers of images
        images = random.sample(images_set, num_box)
        #resize_imgs =[]
        final_image = Image.new('RGB', (416, 416), (128, 128, 128))
        for i, image in enumerate(images):
            print(image)
            img = Image.open(image)

            resize_img = pad_image(img,boxes_size[i])
            #resize_imgs.append(resize_img)
            final_image.paste(resize_img, boxes_size[-1][i])
        return final_image
    else:
        print("Rise error in cutting box")


def detect_faces(image):
    detector = MTCNN()
    faces = [face["box"] for face in detector.detect_faces(image)]
    return faces


def getxywh(face):
    return face[0], face[1], face[2], face[3]


def display_all_faces(image, faces):
    for face in faces:
        box_x, box_y, box_w, box_h = getxywh(face)
        image = cv2.rectangle(image, (box_x, box_y), (box_x + box_w, box_y + box_h), (255, 0, 0))

    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()


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


# base_dir = "C:\\Users\\naiyu\\Documents\\Naiyun"
# csv_dir = "Manually_Annotated_file_lists/.csv"
#
# csv_path = os.path.join(base_dir, csv_dir)
# # subDirectory_filePath	face_x	face_y	face_width	face_height	facial_landmarks	expression	valence	arousal
#
# base_save_path = "../data/NiuTong"
#
# emotion_counter = np.zeros(7)
#
# File_object = open(r"../train_dataset.txt", "w")
#
# with open(csv_path, "r") as f:
#     reader = csv.reader(f, delimiter=",")
#     reader.__next__()
#
#     while reader.__next__() is not None:
#         number = random(1, 2, 4, 9)
#         images_info = []
#         for i in range(number):
#             line = reader.__next__()
#             if line is None:
#                 break
#             else:
#                 images_info.append(line)
#         images_path = []
#
#         for image_info in images_info:
#             image_path = image_info[0]
#             images_path.append(image_path)
#             emotion_id = image_info[6]
#
#         new_image = img_fill(number, images_path)


images = ["data/train/1/1_0.0.jpg","data/train/0/0_0.0.jpg","data/train/0/0_1.0.jpg",
          "data/train/1/1_1.0.jpg","data/train/6/6_0.0.jpg","data/train/6/6_1.0.jpg",
          "data/train/1/1_2.0.jpg","data/train/1/1_3.0.jpg","data/train/0/0_2.0.jpg"]
new_image = img_fill(4,images)
count = 1
new_image.save("train_dataset/"+str(count)+".jpg")
# img = cv2.imread("1.jpg")
# faces = detect_faces(img)
# display_all_faces(img,faces)
# plt.imshow(new_image)
# plt.show()