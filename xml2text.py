import torch
import xml.etree.ElementTree as ET
from glob import glob
import os
import shutil


#paths for test purposes only
root="./datasets/JPEGImages/"
annRoot="./datasets/XMLAnnotations/"
split="./datasets/ImageSplits/"


def build_label_dict(label_src):
    label_dict={}
    c=0
    with open(str(label_src),"r") as f:
        for line in f:
            label_dict[line.rstrip()]=c
            c+=1
    return label_dict

def return_index_for_label(label):
    label_dict=build_label_dict("labels.txt")
    return int(label_dict[label])


def partition_dataset():
    test_dest="./datasets/testset"
    train_dest="./datasets/trainset"
    testfile,trainfile=[],[]
    for filename in os.listdir(split):
        if filename.endswith('test.txt'):
            testfile.append(str(filename))
        if filename.endswith('train.txt'):
            trainfile.append(str(filename))
    for fname in testfile:
        with open(str(split+fname),"r") as f:
            for line in f:
                shutil.copy2(str(root+line.rstrip()),test_dest)
    for fname in trainfile:
        with open(str(split+fname),"r") as f:
            for line in f:
                shutil.copy2(str(root+line.rstrip()),train_dest)
    print("Test and Train sets created!")


def extract_annotations(image_id,annRoot):
    res=[]
    width,height=0,0
    for file in os.listdir(annRoot):
        if file.startswith(image_id.split('.')[0]) and file.endswith('.xml'):
            extract=file
    tree=ET.parse(str(annRoot+extract))
    root=tree.getroot()
    for obj in root.iter('size'):
        width=int(obj.find('width').text)
        height=int(obj.find('height').text)

    for obj in root.iter('object'):
        label_index=return_index_for_label(obj.find('action').text.strip())
        bbox=obj.find('bndbox')
        pts = ['xmin', 'ymin', 'xmax', 'ymax']
        bndbox = []

        for i, pt in enumerate(pts):
            cur_pt = int(bbox.find(pt).text) - 1
            # scale height or width
            cur_pt = cur_pt / width if i % 2 == 0 else cur_pt / height
            bndbox.append(cur_pt)
        bndbox.append(label_index)
    return bndbox



# if __name__ =="__main__":
#     extract_annotations('applauding_001.jpg')
