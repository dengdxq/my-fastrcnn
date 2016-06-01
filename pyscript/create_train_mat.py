#-*- coding:utf-8 –*-
import sys
import os
import dlib
from skimage import io
import numpy as np
import scipy.io as scio



def get_file_list(train_list):
    files = open(train_list, 'r')
    filelist = []
    for text in files.readlines():
        strs = text.split('\n')
        if len(strs) != 2:
            print 'ERROR: %s'%(text)
            continue
        filelist.append(strs[0])
    files.close()
    return filelist

def get_selective_search(imgdir, name, imgtype):
    img = io.imread(imgdir+'/'+name+'.'+imgtype)
    rects = []
    dlib.find_candidate_object_locations(img,rects,min_size=0)
    boxes = []
    for key,value in enumerate(rects):
        elem = [value.top()+1,value.left()+1,value.bottom()+1,value.right()+1]
        boxes.append(elem)
    boxes = np.array(boxes)
    return boxes

def read_matfile(matfile):
    raw_data = scio.loadmat(matfile)['all_boxes'].ravel()
    print raw_data

if __name__ == '__main__':
    #test
    '''
    img_type = 'png'
    img_path = '/Users/wangjj/Documents/download_code/imageset/chars/Images'
    train_img_list = '/Users/wangjj/Documents/download_code/imageset/chars/ImageSets'+'/train.txt'
    save_path = '/Users/wangjj/Documents/download_code/imageset/chars'
    '''
    if len(sys.argv) < 5:
        print "ERROR: not enough arguments"
        print "Example:  python create_train_mat.py train.txt img_dir img_type save_path"
        print "示例: python create_train_mat.py 标注的文件列表 输出xml格式的ground_truth目录 输出train.txt列表文件"
        exit()
    train_img_list = sys.argv[1]
    img_path = sys.argv[2]
    img_type = sys.argv[3]
    save_path = sys.argv[4]

    namelist = get_file_list(train_img_list)
    #print namelist
    allboxes = []
    for name in namelist:
        boxes = get_selective_search(img_path, name, img_type)
        #print boxes
        allboxes.append(boxes)
    scio.savemat(save_path+'/train.mat',mdict={'all_boxes':allboxes})

    #read mat file
    #read_matfile(save_path+'/train_matlab.mat')
