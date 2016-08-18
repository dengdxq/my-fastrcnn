#-*- coding:utf-8 –*-
import matplotlib
matplotlib.use('Agg')
import fastrcnn
import os
import shutil
import random
import time


PROTOTXT = '/data/checkcode/code/my-fastrcnn/models/checkcode_vgg16/test.prototxt'
CAFFEMODEL = '/data/checkcode/code/my-fastrcnn/modelfile/checkcode_vgg16_fast_rcnn_iter_200000.caffemodel'
CLASS_TUPLE = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9')

def get_file_list(path, suffix):
    filelist = []
    for root,dirs,files in os.walk(path):
	for felem in files:
		strs = felem.split('.')
		if len(strs)!=2 or cmp(strs[1],suffix)!=0:
		    continue
	    	filelist.append(felem)
    return filelist


def random_string(strlen):
    alpha_list = ['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a']
    name = random.sample(alpha_list, strlen)
    name = ''.join(name)
    return name


def gpu_recoginze_images(src_img_path):
    global PROTOTXT
    global CAFFEMODEL
    global CLASS_TUPLE
    #load net
    caffe_net = fastrcnn.load_caffe_net(PROTOTXT, CAFFEMODEL, 1)
    imglist = get_file_list(src_img_path, 'jpg')
    num = len(imglist)
    cnt = 0
    cnt1 = 0
    max_time = 0
    start_time = time.time()
    for i in range(0,num):
        #print 'process: %d'%(i+1)
        imgpath = src_img_path + '/' + imglist[i]        
        if os.path.exists(imgpath)==False:
            continue
        strs = imglist[i].split('_')
        label = strs[0]
        t1 = time.time()
        cc_value = fastrcnn.recognize_checkcode_img(caffe_net, imgpath, CLASS_TUPLE)
        t2 = time.time()
        t = t2 - t1
        if t > max_time:
            max_time = t
        if cmp(cc_value['ccvalue'].lower(), label.lower())==0:
            cnt1 += 1
        cnt += 1
    end_time = time.time()
        #print imgpath
        #print cc_value['ccvalue']
    print 'total=%d, acc=%d'%(cnt, cnt1)
    print 'total time=%f'%(end_time-start_time)
    print 'max time=%f'%(max_time)
    print 'gpu_recoginze_images: %f'%(1.0*cnt1/cnt)

def cpu_recoginze_images(src_img_path):
    global PROTOTXT
    global CAFFEMODEL
    global CLASS_TUPLE
    #load net
    caffe_net = fastrcnn.load_caffe_net(PROTOTXT, CAFFEMODEL, 0)
    imglist = get_file_list(src_img_path, 'jpg')
    num = len(imglist)
    cnt = 0
    cnt1 = 0
    max_time = 0
    start_time = time.time()
    for i in range(0,num):
        print 'process: %d'%(i+1)
        imgpath = src_img_path + '/' + imglist[i]        
        if os.path.exists(imgpath)==False:
            continue
        strs = imglist[i].split('_')
        label = strs[0]
        t1 = time.time()
        cc_value = fastrcnn.recognize_checkcode_img(caffe_net, imgpath, CLASS_TUPLE)
        t2 = time.time()
        t = t2 - t1
        print 'time = %f'%(t)
        if t > max_time:
            max_time = t
        if cmp(cc_value['ccvalue'].lower(), label.lower())==0:
            cnt1 += 1
        cnt += 1
    end_time = time.time()
        #print imgpath
        #print cc_value['ccvalue']
    print 'total=%d, acc=%d'%(cnt, cnt1)
    print 'total time=%f'%(end_time-start_time)
    print 'max time=%f'%(max_time)
    print 'cpu_recoginze_images: %f'%(1.0*cnt1/cnt)


if __name__=='__main__':
    #label_images('/data/Images/checkcode/data/TestImgs2', '/data/Images/checkcode/data/TestImgs_label2')
    path = '/data/checkcode/0_f1'
    gpu_recoginze_images(path)
    #cpu_recoginze_images(path)
