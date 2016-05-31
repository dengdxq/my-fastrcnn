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
import shutil
import math



CLASSES = ('__background__','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9')


def vis_detections(class_name, dets, thresh=0.5):
    """Draw detected bounding boxes."""
    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return []
    str = ''
    charbox_list = [];
    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]
        '''
        str += class_name
        if bbox[0]>170:
            xmin = 169
        else:
            xmin = int(bbox[0])

        if bbox[1]>60:
            ymin = 59
        else:
            ymin = int(bbox[1])

        if bbox[2]>170:
            xmax = 169
        else:
            xmax = int(bbox[2])

        if bbox[3]>60:
            ymax = 59
        else:
            ymax = int(bbox[3])
        '''
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
        charbox_list.append({'char':class_name, 'xoffset':bbox[0], 'xmin':xmin, 'ymin':ymin, 'xmax':xmax, 'ymax':ymax});

        '''
        ax.add_patch(
            plt.Rectangle((bbox[0], bbox[1]),
                          bbox[2] - bbox[0],
                          bbox[3] - bbox[1], fill=False,
                          edgecolor='red', linewidth=3.5)
            )
        ax.text(bbox[0], bbox[1] - 2,
                '{:s} {:.3f}'.format(class_name, score),
                bbox=dict(facecolor='blue', alpha=0.5),
                fontsize=14, color='white')
        '''
    #plt.axis('off')
    #plt.tight_layout()
    #plt.draw()
    return charbox_list



def demo(net, image_name, box_file, out_img, classes):
    obj_proposals = sio.loadmat(box_file)['boxes']
    # Load the demo image
    im_file = image_name
    im = cv2.imread(im_file)
    # Detect all object classes and regress object bounds
    scores, boxes = im_detect(net, im, obj_proposals)
    # Visualize detections for each class
    CONF_THRESH = 0.8
    NMS_THRESH = 0.3
    img = im[:, :, (2, 1, 0)]
    data_list = [];
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
        tmplist = vis_detections(cls, dets, thresh=CONF_THRESH)
        if len(tmplist) == 0:
            continue
        data_list.extend(tmplist)
    data_list.sort(key=lambda obj:obj.get('xoffset'), reverse=False)
    str = ''
    for elem in data_list:
        str = str + elem.get('char')
    return str


def recognize(net, image_name, box_file, classes):
    obj_proposals = sio.loadmat(box_file)['boxes']
    # Load the demo image
    im_file = image_name#os.path.join(cfg.ROOT_DIR, 'data', 'demo', image_name + '.jpg')
    im = cv2.imread(im_file)
    # Detect all object classes and regress object bounds
    timer = Timer()
    timer.tic()
    scores, boxes = im_detect(net, im, obj_proposals)
    timer.toc()
    print ('Detection took {:.3f}s for '
           '{:d} object proposals').format(timer.total_time, boxes.shape[0])

    # Visualize detections for each class
    CONF_THRESH = 0.8
    NMS_THRESH = 0.3
    img = im[:, :, (2, 1, 0)]
    data_list = [];
    for cls in classes:
        cls_ind = CLASSES.index(cls)
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        keep = np.where(cls_scores >= CONF_THRESH)[0]
        #print cls
        #print keep
        #print '================='
        cls_boxes = cls_boxes[keep, :]
        cls_scores = cls_scores[keep]
        dets = np.hstack((cls_boxes, cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        #print type(dets[0,:])
        #print '====='
        #print len(dets)
        tmplist = vis_detections(cls, dets, thresh=CONF_THRESH)
        if len(tmplist) == 0:
            continue
        data_list.extend(tmplist)
    data_list.sort(key=lambda obj:obj.get('xoffset'), reverse=False)
    '''
    str = ''
    for elem in data_list:
        str = str + elem.get('char')
    return str
    '''
    return data_list


if __name__ == '__main__':
    inputdir = '/home/jiayuan/Documents/checkcode/data/validimgs'
    outputdir = '/home/jiayuan/Documents/checkcode/data/validres'
    boxdir = '/home/jiayuan/Documents/checkcode/data/ssbox'
    prototxt = '/home/jiayuan/Documents/download_code/fast-rcnn/models/checkcode/test.prototxt'
    caffemodel = '/home/jiayuan/Documents/download_code/fast-rcnn/data/fast_rcnn_models/checkcode_fast_rcnn_iter_100000.caffemodel'
    #caffe.set_mode_cpu()
    caffe.set_mode_gpu()
    caffe.set_device(0)
    net = caffe.Net(prototxt, caffemodel, caffe.TEST)
    class_tuple = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9')    
    #
    files = os.listdir(inputdir)
    pfile = open('/home/jiayuan/Documents/checkcode/data/imglist.txt', 'w')
    for file in files:        
        strs = file.split('.')
        if len(strs) < 2:
            continue
        img_name = inputdir + '/' + file
        box_file = boxdir + '/' + strs[0] + '_boxes.mat'
        if os.path.isfile(img_name)==False:
            print 'No Exist: ' + img_name
            continue
            
        if os.path.isfile(box_file)==False:
            print 'No Exist: ' + box_file
            continue
        print img_name
        reslist = recognize(net, img_name, box_file, class_tuple)
        res = ''
        for elem in reslist:
            res = res + elem.get('char')
        shutil.copyfile(img_name, outputdir+'/'+res+'.jpg')
        #write
        pfile.write(file+' '+res+' '+str(len(res)))
        for elem in reslist:
            pfile.write(' '+str(elem.get('xmin'))+' '+str(elem.get('ymin'))+' '+str(elem.get('xmax'))+' '+str(elem.get('ymax')))    
        
        pfile.write('\n')
    print 'complete!'
