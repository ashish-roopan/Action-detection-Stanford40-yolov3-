import xml.etree.ElementTree as ET
from glob import glob
import os
import shutil







image_root="./Stanford40/JPEGImages/"
ann_root="./Stanford40/XMLAnnotations/"
split="./Stanford40/ImageSplits/"
test_dest="./Stanford40/test"
train_dest="./Stanford40/train"
test_ann_dest="./Stanford40/test_ann"
train_ann_dest="./Stanford40/train_ann"

testfile,trainfile=[],[]
for filename in os.listdir(split):
    if filename.endswith('test.txt'):
        testfile.append(str(filename))
    if filename.endswith('train.txt'):
        trainfile.append(str(filename))
for fname in testfile:
        with open(str(split+fname),"r") as f:
            for line in f:
                shutil.copy2(str(image_root+line.rstrip()),test_dest)
                line=line.split('.')[0] +'.xml'
                shutil.copy2(str(ann_root+line),test_ann_dest)
for fname in trainfile:
        with open(str(split+fname),"r") as f:
            for line in f:
                shutil.copy2(str(image_root+line.rstrip()),train_dest)
                line=line.split('.')[0] +'.xml'
                shutil.copy2(str(ann_root+line),train_ann_dest)
print("Test and Train sets created!")
