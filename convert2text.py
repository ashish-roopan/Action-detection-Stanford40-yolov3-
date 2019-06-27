
import os
import xml.etree.ElementTree as ET
from os import getcwd



classes=['applauding','blowing_bubbles','brushing_teeth','cleaning_the_floor','climbing','cooking','cutting_trees','cutting_vegetables','drinking','feeding_a_horse','fishing','fixing_a_bike','fixing_a_car','gardening','holding_an_umbrella','jumping','looking_through_a_microscope','looking_through_a_telescope','playing_guitar','playing_violin','pouring_liquid','pushing_a_cart','reading','phoning','riding_a_bike','riding_a_horse','rowing_a_boat','running','shooting_an_arrow','smoking',
'taking_photos','texting_message','throwing_frisby','using_a_computer','walking_the_dog','washing_dishes','watching_TV','waving_hands','writing_on_a_board','writing_on_a_book']

print(len(classes))




def convert_annotations(filename,list_file):
    filename=filename.split('.')[0]
    in_file = open('Stanford40/train_ann/%s.xml'%(filename))
    tree=ET.parse(in_file)
    root=tree.getroot()

    for obj in root.iter('object'):

        cls = obj.find('action').text
        if cls not in classes:
            continue
        cls_id=classes.index(cls)

        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))







list_file = open('annotations.txt', 'w')
for filename in os.listdir('Stanford40/train'):

    list_file.write('Stanford40/train/%s'%( filename))
    convert_annotations(filename,list_file)
    list_file.write('\n')
list_file.close()
