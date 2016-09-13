#-*- coding:utf-8 –*-

import os.path as osp
import sys

prototxt = '/data/checkcode/code/my-fastrcnn/models/checkcode_vgg16/test.prototxt'
#caffemodel = '/data/checkcode/code/my-fastrcnn/modelfile/checkcode_vgg16_fast_rcnn_iter_200000.caffemodel'
caffemodel = '/data/checkcode/code/my-fastrcnn/modelfile/checkcode_vgg16_all_iter_200000.caffemodel'
############################
#IMAGE
############################
img_save_dir = '/data/checkcode/imgs'
img_max_num = 5000
############################
#LOG
############################
log_file = '/data/checkcode/logs'
log_file_size = 104857600 #100M=1024*1024*100
log_file_name = 'checkcode.log'
log_file_max_num = 50
############################
#
############################
#type_black_list = ['nanchong','taizhou','baoding']
type_black_list = ['']
