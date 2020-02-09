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
    img = Image.open(image[0])
    iw, ih = img.size  # 原始图像的尺寸
    w, h = target_size  # 目标图像的尺寸
    print(iw, ih, target_size)
    rw = float(w) / float(iw)
    rh = float(h) / float(ih)
    scale = min(rw, rh)  # 转换的最小比例

    # 保证长或宽，至少一个符合目标图像的尺寸
    nw = int(iw * scale)
    nh = int(ih * scale)
    img = img.resize((nw, nh), Image.BICUBIC)  # 缩小图像
    # image.show()
    new_image = Image.new('RGB', (w,h), (128, 128, 128))  # 生成灰色图像
    # // 为整数除法，计算图像的位置
    new_image.paste(img, ((w - nw) // 2, (h - nh) // 2))  # 将图像填充为中间图像，两侧为灰色的样式
    #new_image.paste(image, (30,0))
    face_left = int(scale*image[1])
    face_top = int(scale * image[2])
    face_right = int(scale * image[3])
    face_bot = int(scale * image[4])
    face = [new_image,face_left,face_top,face_right,face_bot]
    # new_image.show()

    return face

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

def img_fill(num_box,images,faces_info):
    target_size = [416,416]
    boxes_size = cut_box(num_box,target_size)
    if num_box == len(boxes_size)-1:
        #resize_imgs =[]
        final_image = Image.new('RGB', (416, 416), (128, 128, 128))
        all_faces = []
        for i, image in enumerate(faces_info):

            #img = Image.open(image[0])
            face = pad_image(image,boxes_size[i])
            resize_img = face[0]
            #resize_imgs.append(resize_img)
            final_image.paste(resize_img, boxes_size[-1][i])
            #the size of box
            box_w,box_h = boxes_size[i]
            #the location of left-corner of box.(x,y)
            box_x,box_y = boxes_size[-1][i]
            #image_loc = the location of left-corner of image.
            if box_w>box_h:
                image_loc = [box_x+(box_w-box_h)/2,box_y]
            elif box_w<box_h:
                image_loc = [box_x,box_y+(box_h-box_w)/2]
            elif:
                image_loc = [box_x,box_y]
            x,y = image_loc
            left = face[1]+x
            top = face[2]+y
            right = face[3]+x
            bottom = face[4]+y
            emotion = image[5]
            data = [left,top,right,bottom,emotion]
            all_faces.append(data)
        final_info = [final_image, all_faces]
        return final_info
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


base_dir = "C:\\Users\\naiyu\\Documents\\Naiyun"
csv_dir = "Manually_Annotated_file_lists/validation_dataset.csv"
image_dir = "Manually_Annotated/Manually_Annotated_Images"
csv_path = os.path.join(base_dir, csv_dir)
# subDirectory_filePath	face_x	face_y	face_width	face_height	facial_landmarks	expression	valence	arousal

base_save_path = "data/"

emotion_counter = np.zeros(7)

File_object = open(r"validation_dataset.txt", "w")

with open(csv_path, "r") as f:
    reader = csv.reader(f, delimiter=",")
    reader.__next__()

    while reader.__next__() is not None:
        number = random(1, 2, 4, 9)
        count = 0
        images_info = []
        for i in range(number):
            line = reader.__next__()
            if line is None:
                break
            else:
                images_info.append(line)
        # face_info has the path of image the location of face (left,top,right,bottom), and the emotion label.
        faces_info = []
        for image_info in images_info:
            image_path = image_info[0]
            image_final_path = os.path.join(base_dir,image_dir,image_path)
            face_x = image_info[1]
            face_y = image_info[2]
            face_w = image_info[3]
            face_h = image_info[4]
            emotion_id = image_info[6]
            face_info = [image_final_path, face_x,face_x + face_w, face_y, face_y + face_h, emotion_id]
            faces_info.append(face_info)


        data_info = img_fill(number, faces_info)
        new_image = data_info[0]
        new_image.save("data/"+str(count)+".jpg")
        count += 1

# images = ["data/train/1/1_0.0.jpg","data/train/0/0_0.0.jpg","data/train/0/0_1.0.jpg",
#           "data/train/1/1_1.0.jpg","data/train/6/6_0.0.jpg","data/train/6/6_1.0.jpg",
#           "data/train/1/1_2.0.jpg","data/train/1/1_3.0.jpg","data/train/0/0_2.0.jpg"]
# img = cv2.imread("1.jpg")
# faces = detect_faces(img)
# display_all_faces(img,faces)
# plt.imshow(new_image)
# plt.show()