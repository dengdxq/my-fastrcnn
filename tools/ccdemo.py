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


class Iterm(object):
    def __init__(self):
        self.char = ''
        self.x = 0

CLASSES = ('__background__','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9')


def vis_detections(ax, class_name, dets, thresh=0.5):
    """Draw detected bounding boxes."""
    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return []
    charbox_list = [];
    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]
        print '-=-==-='
        print class_name
        print '-=-==-='
        charbox_list.append({'char':class_name, 'xoffset':bbox[0]});
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
    plt.axis('off')
    #plt.tight_layout()
    plt.draw()
    return charbox_list



def demo(net, image_name, box_file, out_img, classes):
    obj_proposals = sio.loadmat(box_file)['boxes']
    # Load the demo image
    im_file = image_name#os.path.join(cfg.ROOT_DIR, 'data', 'demo', image_name + '.jpg')
    im = cv2.imread(im_file)
    # Detect all object classes and regress object bounds
    timer = Timer()
    timer.tic()
    scores, boxes = im_detect(net, im, obj_proposals)
    #print type(boxes)
    dims = boxes.shape
    print dims
    rows = dims[0]
    cols = dims[1]
    #for elem in boxes.flat:
    #	print elem
    print '-===-=-==-==-=-====================--------'
    timer.toc()
    print ('Detection took {:.3f}s for '
           '{:d} object proposals').format(timer.total_time, boxes.shape[0])

    # Visualize detections for each class
    CONF_THRESH = 0.85
    NMS_THRESH = 0.3
    img = im[:, :, (2, 1, 0)]
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(im, aspect='equal')
    data_list = [];
    for cls in classes:    	
        cls_ind = CLASSES.index(cls)
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
        #print cls_boxes
        #print '================='
        cls_scores = scores[:, cls_ind]
        keep = np.where(cls_scores >= CONF_THRESH)[0]
        #print cls
        cls_boxes = cls_boxes[keep, :]

        cls_scores = cls_scores[keep]
        dets = np.hstack((cls_boxes, cls_scores[:, np.newaxis])).astype(np.float32)

        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        
        tmplist = vis_detections(ax, cls, dets, thresh=CONF_THRESH)
        if len(tmplist) == 0:
            continue
        data_list.extend(tmplist)
    print data_list
    print '====================='
    plt.savefig(out_img)
    data_list.sort(key=lambda obj:obj.get('xoffset'), reverse=False)
    str = ''
    for elem in data_list:
        str = str + elem.get('char')
    return str


if __name__ == '__main__':
    
    prototxt = '/home/jiayuan/Documents/download_code/fast-rcnn/models/checkcode/test.prototxt'
    caffemodel = '/home/jiayuan/Documents/download_code/fast-rcnn/data/fast_rcnn_models/checkcode_fast_rcnn_iter_200000.caffemodel'
    caffe.set_mode_cpu()
    #caffe.set_mode_gpu()
    #caffe.set_device(0)
    net = caffe.Net(prototxt, caffemodel, caffe.TEST)
    class_tuple = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9')
    #class_tuple = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M')
    img_name = '/home/jiayuan/Documents/download_code/fast-rcnn/data/demo/192.jpg'
    box_file = '/home/jiayuan/Documents/download_code/fast-rcnn/data/demo/192.mat'
    str = demo(net, img_name, box_file, '/home/jiayuan/Documents/download_code/fast-rcnn/result.jpg',class_tuple)
    print 'result={}'.format(str)
