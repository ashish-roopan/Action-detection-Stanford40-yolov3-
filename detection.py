import sys
import argparse
from yolo import YOLO, detect_video
from PIL import Image
from glob import glob
import os
import cv2
import numpy as np
import xml.etree.ElementTree as ET
from os import getcwd


classes=['applauding','blowing_bubbles','brushing_teeth','cleaning_the_floor','climbing','cooking','cutting_trees','cutting_vegetables','drinking','feeding_a_horse','fishing','fixing_a_bike','fixing_a_car','gardening','holding_an_umbrella','jumping','looking_through_a_microscope','looking_through_a_telescope','playing_guitar','playing_violin','pouring_liquid','pushing_a_cart','reading','phoning','riding_a_bike','riding_a_horse','rowing_a_boat','running','shooting_an_arrow','smoking',
'taking_photos','texting_message','throwing_frisby','using_a_computer','walking_the_dog','washing_dishes','watching_TV','waving_hands','writing_on_a_board','writing_on_a_book']



def gnd_truth_generate():
    for filename in os.listdir('./Stanford40/test_ann/'):
            xml_file=open('./Stanford40/test_ann/'+filename,'r')
            filename=filename.split('.')[0]
            #filename=filename[:-4]
            txt_file=open('./mAP/input/ground-truth/'+filename+'.txt','w')
            r_txt_file=open('./mAP/input/detection-results/'+filename+'.txt','w')

            tree=ET.parse(xml_file)

            root=tree.getroot()

            for obj in root.iter('object'):

                cls = obj.find('action').text
                if cls not in classes:
                    continue
                cls_id=classes.index(cls)
                print(cls)

                xmlbox = obj.find('bndbox')
                left=xmlbox.find('xmin').text
                top=xmlbox.find('ymin').text
                right=xmlbox.find('xmax').text
                bottom=xmlbox.find('ymax').text

                txt_file.write(cls+' '+str(left)+ ' ' +str(top)+ " "+str(right)+' '+str(bottom)+'\n')
                txt_file.close()

                #b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
                #list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))





def detect_img(yolo):

        gnd_truth_generate()
        #img = input('Input image filename:')
        for filename in os.listdir('./Stanford40/test/'):
            print(filename)
            img='Stanford40/test/'+filename
            try:
                image = Image.open(img)

            except:
                print('Open Error! Try again!')
                #continue
            else:

                r_image = yolo.detect_image(image,filename)
                #r_image.show()
                '''img=np.array(r_image)
                img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                cv2.imshow('img',img)
                q=cv2.waitKey(2)
                if q==ord('q'):
                    break'''
        yolo.close_session()
        cv2.destroyAllWindows()
FLAGS = None

if __name__ == '__main__':

    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    parser.add_argument(
        '--model', type=str,
        help='path to model weight file, default ' + YOLO.get_defaults("model_path")
    )

    parser.add_argument(
        '--anchors', type=str,
        help='path to anchor definitions, default ' + YOLO.get_defaults("anchors_path")
    )

    parser.add_argument(
        '--classes', type=str,
        help='path to class definitions, default ' + YOLO.get_defaults("classes_path")
    )

    parser.add_argument(
        '--gpu_num', type=int,
        help='Number of GPU to use, default ' + str(YOLO.get_defaults("gpu_num"))
    )

    parser.add_argument(
        '--image', default=False, action="store_true",
        help='Image detection mode, will ignore all positional arguments'
    )
    '''
    Command line positional arguments -- for video detection mode
    '''
    parser.add_argument(
        "--input", nargs='?', type=str,required=False,default='./path2your_video',
        help = "Video input path"
    )

    parser.add_argument(
        "--output", nargs='?', type=str, default="",
        help = "[Optional] Video output path"
    )

    FLAGS = parser.parse_args()
    print(FLAGS)

    if FLAGS.image:
        """
        Image detection mode, disregard any remaining command line arguments
        """
        print("Image detection mode")
        if "input" in FLAGS:
            print(" Ignoring remaining command line arguments: " + FLAGS.input + "," + FLAGS.output)
        detect_img(YOLO(**vars(FLAGS)))
    elif "input" in FLAGS:
        detect_video(YOLO(**vars(FLAGS)), FLAGS.input, FLAGS.output)
    else:
        print("Must specify at least video_input_path.  See usage with --help.")
