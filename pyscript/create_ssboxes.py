#-*- coding:utf-8 –*-
import sys
import os
import dlib
from skimage import io
import numpy as np
import scipy.io as scio


def get_boxes_batch(list_filename, imgdir, savepath):
    pfile = open(list_filename, 'r')
    for text in pfile.readlines():
        string = text.strip('\n')
        strs = string.split(' ')
        filename = strs[0]
        if os.path.exists(imgdir+'/'+filename)==False:
            print '[ERROR]: %s is not exist!'%(filename)
            continue
        boxes = get_selective_search_boxes(imgdir, filename)
        if boxes==None:
            print '[ERROR]: %s can not get boxed!'%(filename)
            continue
        names = strs[0].split('.')
        scio.savemat(savepath+'/'+names[0]+'.mat', mdict={'boxes':boxes})


def get_selective_search_boxes(imgdir, name):
    filepath = imgdir+'/'+name
    if os.path.exists(filepath)==False:
        print '[ERROR]: %s is not exist!'%(filepath)
        return None
    img = io.imread(filepath)
    rects = []
    dlib.find_candidate_object_locations(img,rects,min_size=0)
    boxes = []
    for key,value in enumerate(rects):
        elem = [value.left()+1, value.top()+1, value.right()+1, value.bottom()+1]
        boxes.append(elem)
    boxes = np.array(boxes)
    return boxes

if __name__=='__main__':
    if len(sys.argv) < 3:
        print "ERROR: not enough arguments"
        print "Example:  python create_ssboxes.py imglist.txt img_dir save_path"
        print "示例: python create_ssboxes.py 标注的文件列表 图片目录 输出所有文件的ssbox"
        exit()
    img_list = sys.argv[1]
    img_path = sys.argv[2]
    save_path = sys.argv[3]
    get_boxes_batch(img_list, img_path, save_path)
