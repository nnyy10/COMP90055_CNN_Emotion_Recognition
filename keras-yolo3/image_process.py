import cv2
from PIL import Image,ImageDraw
from matplotlib import pyplot as plt
from mtcnn import MTCNN
import random
import csv
import os
"""
 This script can randomly put 1,2,4,9 original images(just faces) to one image.
 Also Output .txt file including image_path, bouding boxes ([x_min,y_min,x_max,y_max]),and class_id
"""


def pad_image(image, target_size):
    print("image_path",image[0])
    img = Image.open(image[0])
    iw, ih = img.size  # orginal size
    w, h = target_size  # target size
    print(img.size, target_size)
    rw = float(w) / float(iw)
    rh = float(h) / float(ih)
    scale = min(rw, rh)  #

    nw = int(iw * scale)
    nh = int(ih * scale)
    img = img.resize((nw, nh), Image.BICUBIC)  # resize of imgae
    # image.show()
    new_image = Image.new('RGB', (w,h), (128, 128, 128))  # create grey scale image.

    #Fill image into the center of the new_image.
    new_image.paste(img, ((w - nw) // 2, (h - nh) // 2))

    face_left = scale*int(image[1])
    face_top = scale * int(image[2])
    face_right = scale * int(image[3])
    face_bot = scale * int(image[4])
    face = [new_image,face_left,face_top,face_right,face_bot]

    return face


# cut box in to 1,2,4,9 rectangle areas.
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

def img_fill(num_box,faces_info):
    target_size = [416,416]
    boxes_size = cut_box(num_box,target_size)
    if num_box == len(boxes_size)-1:
        final_image = Image.new('RGB', (416, 416), (128, 128, 128))
        all_faces = []
        for i, image in enumerate(faces_info):
            face = pad_image(image,boxes_size[i])
            resize_img = face[0]

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
            else:
                image_loc = [box_x,box_y]
            x,y = image_loc
            left = int(x+face[1])
            top = int(y+face[2])
            right = int(x+face[3])
            bottom = int(y+face[4])
            emotion = int(image[5])
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


def list2str(lists):
    comma = ","
    str2 = ""
    for list in lists:
        str1 = comma.join(str(i) for i in list)
        str2 += str1+" "
    str3 = str2[0:-1]
    return  str3


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
csv_dir = "Manually_Annotated_file_lists/training_dataset.csv"
image_dir = "Manually_Annotated/Manually_Annotated_Images"
csv_path = os.path.join(base_dir, csv_dir)
# subDirectory_filePath	face_x	face_y	face_width	face_height	facial_landmarks	expression	valence	arousal

File_object = open(r"train.txt", "w")


with open(csv_path, "r") as f:
    reader = csv.reader(f, delimiter=",")
    line = reader.__next__()
    count = 0
    while line is not None:
        number = random.choice([1, 2, 4, 9])
        images_info = []
        images_info.append(line)
        for i in range(number-1):
            line = reader.__next__()
            if line is None:
                break
            else:
                images_info.append(line)
        line = reader.__next__()
        # face_info has the path of image the location of face (left,top,right,bottom), and the emotion label.
        faces_info = []
        for image_info in images_info:
            image_path = image_info[0]
            image_final_path = os.path.join(base_dir,image_dir,image_path)
            face_x = int(image_info[1])
            face_y = int(image_info[2])
            face_w = int(image_info[3])
            face_h = int(image_info[4])
            emotion_id = image_info[6]
            face_info = [image_final_path, face_x,face_y, face_x+face_w, face_y + face_h, emotion_id]
            print(face_info)
            faces_info.append(face_info)

        data_info = img_fill(number, faces_info)
        new_image = data_info[0]
        boxes = data_info[1]
        save_img_path = "data/train/"+str(count)+".jpg"
        new_image.save(save_img_path)

        info = list2str(boxes)
        write_line = save_img_path+" "+info+"\n"
        File_object.write(write_line)
        count += 1
        print(str(count)+":"+write_line)

