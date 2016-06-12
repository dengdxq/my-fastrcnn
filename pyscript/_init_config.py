#-*- coding:utf-8 –*-

import os.path as osp
import sys

prototxt = '/data/code/my-fastrcnn/models/checkcode_vgg16/test.prototxt'
caffemodel = '/data/code/my-fastrcnn/output/default/train.1/checkcode_vgg16_fast_rcnn_iter_110000.caffemodel'
############################
#IMAGE
############################
img_save_dir = '/data/tmp/images'
img_max_num = 5000
############################
#LOG
############################
log_file = '/data/tmp/logs'
log_file_size = 104857600 #100M=1024*1024*100
log_file_name = 'checkcode.log'
log_file_max_num = 50

