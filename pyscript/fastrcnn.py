#-*- coding:utf-8 –*-
#!/usr/bin/env python

# --------------------------------------------------------
# Fast R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""
Demo script showing detections in sample images.

See README.md for installation instructions before running.
"""

import _init_paths
from fast_rcnn.config import cfg
from fast_rcnn.test_cc import im_detect
from utils.cython_nms import nms
from utils.timer import Timer
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import caffe, os, sys, cv2
import argparse
import dlib
from skimage import io
import scipy.io as scio
import math
import logging
import _init_config
import logconfig


CLASSES = ('__background__','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9')


def get_detection_box(class_name, dets, thresh=0.5):
    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return []
    charbox_list = []
    for i in inds:
        bbox = dets[i, :4]
        score = dets[i,4]
        if math.isnan(bbox[0]) or math.isnan(bbox[1]) or math.isnan(bbox[2]) or math.isnan(bbox[3]):
            return []
        xmin = int(bbox[0])
        ymin = int(bbox[1])
        xmax = int(bbox[2])
        ymax = int(bbox[3])
        if xmax==160:
            xmax = 159
        if ymax==60:
            ymax = 59
        charbox_list.append({'char':class_name, 'xoffset':bbox[0], 'xmin':xmin, 'ymin':ymin, 'xmax':xmax, 'ymax':ymax, 'score':score});
    return charbox_list



def recognize_img(net, image_name, box_file, classes):
    obj_proposals = sio.loadmat(box_file)['boxes']
    # Load the demo image
    im = cv2.imread(image_name)
    # Detect all object classes and regress object bounds
    scores, boxes = im_detect(net, im, obj_proposals)
    #print type(boxes)
    #dims = boxes.shape
    #rows = dims[0]
    #cols = dims[1]

    # Visualize detections for each class
    CONF_THRESH = 0.85
    NMS_THRESH = 0.3
    data_list = []
    for cls in classes:    	
        cls_ind = CLASSES.index(cls)
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        keep = np.where(cls_scores >= CONF_THRESH)[0]
        cls_boxes = cls_boxes[keep, :]
        cls_scores = cls_scores[keep]
        dets = np.hstack((cls_boxes, cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        tmplist = get_detection_box(cls, dets, thresh=CONF_THRESH)
        if len(tmplist) == 0:
            continue
        data_list.extend(tmplist)
    data_list.sort(key=lambda obj:obj.get('xoffset'), reverse=False)
    #data_list = char_roi_filter(data_list)
    str = ''
    for elem in data_list:
        str = str + elem.get('char')
    return str


def recognize_checkcode_img(net, image_name, classes):
    boxes = get_selective_search_boxes(image_name)
    if boxes == None:
        return None
    im = cv2.imread(image_name)
    scores, boxes = im_detect(net, im, boxes)
    CONF_THRESH = 0.85
    NMS_THRESH = 0.3
    data_list = []
    for cls in classes:
        cls_ind = CLASSES.index(cls)
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        keep = np.where(cls_scores >= CONF_THRESH)[0]
        cls_boxes = cls_boxes[keep, :]
        cls_scores = cls_scores[keep]
        dets = np.hstack((cls_boxes, cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        tmplist = get_detection_box(cls, dets, thresh=CONF_THRESH)
        if len(tmplist) == 0:
            continue
        data_list.extend(tmplist)
    data_list.sort(key=lambda obj:obj.get('xoffset'), reverse=False)
    #print 'len1 = %d'%(len(data_list))
    #str = ''
    #for elem in data_list:
    #    str = str + elem.get('char')
    #print str
    #data_list = char_roi_filter(data_list)
    #print 'len2 = %d'%(len(data_list))
    #print data_list
    str = ''
    for elem in data_list:
        str = str + elem.get('char')
    #print data_list
    #print str
    #print '-=-=-=-='
    dict = {}
    dict['ccvalue'] = str
    dict['rects'] = data_list
    data_string = json.dumps(dict)
    print data_string
    return dict


def load_caffe_net(prototxt, caffemodel, issetgpu):
    if issetgpu==1:
        caffe.set_mode_gpu()
        caffe.set_device(0)
    else:
        caffe.set_mode_cpu()
    net = caffe.Net(prototxt, caffemodel, caffe.TEST)

    return net


def get_selective_search_boxes(imgpath):
    if os.path.exists(imgpath)==False:
        print '[ERROR]: %s is not exist!'%(imgpath)
        return None
    img = io.imread(imgpath)
    rects = []
    dlib.find_candidate_object_locations(img,rects,min_size=0)
    boxes = []
    for key,value in enumerate(rects):
        elem = [value.left()+1, value.top()+1, value.right()+1, value.bottom()+1]
        boxes.append(elem)
    if len(boxes) == 0:
        return None
    boxes = np.array(boxes)
    return boxes

#计算两个rect之间的重叠面积
def calc_rect_overlap(rectelem1, rectelem2):
    width = rectelem1['xmax'] - rectelem2['xmin']
    height = rectelem1['ymax'] - rectelem2['ymin']
    if width<=0 or height<=0:
        return 0
    rect1_w = rectelem1['xmax'] - rectelem1['xmin']
    rect1_h = rectelem1['ymax'] - rectelem1['ymin']
    return (1.0*height*width/(rect1_w*rect1_h))

#筛选rect
def char_roi_filter(rectlist):
    n = len(rectlist)
    datalist = []
    idx1 = 0
    idx2 = 0
    while True:
        if idx1 >= n:
            break
        elif idx1 == n-1:
            datalist.append(rectlist[idx1])
            break
        idx2 = idx1 + 1
        #print '%d---%d'%(idx1,idx2)
        area = calc_rect_overlap(rectlist[idx1], rectlist[idx2])      
        #print area  
        if area < 0.5:
            datalist.append(rectlist[idx1])
            idx1 += 1
            continue
        score1 = rectlist[idx1]['score']
        score2 = rectlist[idx2]['score']
        if score1>score2:
            datalist.append(rectlist[idx1])
        else :
            datalist.append(rectlist[idx2])
        idx1 += 2
    return datalist

if __name__ == '__main__':
    prototxt = '/data/code/my-fastrcnn/models/checkcode_vgg16/test.prototxt'
    caffemodel = '/data/code/my-fastrcnn/output/default/train_1w-10w_999zhang/checkcode_vgg16_fast_rcnn_iter_100000.caffemodel'
    imgpath = '/data/Images/checkcode/data/Images/V66wPn0abMUQcGfqOvg4AMU0vynYwNtLdYbha2v2yCi3q4xzfQk.jpg'
    CLASS_TUPLE = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9')
    CAFFE_NET = load_caffe_net(prototxt, caffemodel, 1)
    str = recognize_checkcode_img(CAFFE_NET, imgpath, CLASS_TUPLE)
    print str
    
