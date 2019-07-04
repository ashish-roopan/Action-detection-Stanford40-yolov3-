
import os



gnd_t_folder='mAP/input/ground-truth/'
det_res_folder='mAP/input/detection-results/'


#----path---------/class_name----------/---bbox---------
#Stanford40/train/fixing_a_bike_189.jpg 181,58,300,377,11

for filename in os.listdir(det_res_folder):

    if filename.split('.')[1]=='jpg':
        if os.path.exists(det_res_folder+filename.split('.')[0]+'.txt'):
            print(det_res_folder+filename.split('.')[0]+'.txt')

            os.remove(det_res_folder+filename.split('.')[0]+'.txt')

    new_name=filename.split('.')[0]+'.txt'
    os.rename(det_res_folder+filename,det_res_folder+ new_name) 
