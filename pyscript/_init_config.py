#-*- coding:utf-8 –*-

import os.path as osp
import sys

prototxt = '/home/jiayuan/Documents/download_code/fast-rcnn/models/checkcode/test.prototxt'
caffemodel = '/home/jiayuan/Documents/download_code/fast-rcnn/data/fast_rcnn_models/checkcode_fast_rcnn_iter_200000.caffemodel'
############################
#IMAGE
############################
img_save_dir = '/home/jiayuan/Documents/fastrcnn/images'
img_max_num = 5000
############################
#LOG
############################
log_file = '/home/jiayuan/Documents/fastrcnn/logs'
log_file_size = 104857600 #100M=1024*1024*100
log_file_name = 'checkcode.log'
log_file_max_num = 50

