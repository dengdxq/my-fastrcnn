#-*- coding:utf-8 –*-
import fastrcnn
import os
import shutil
import random


PROTOTXT = '/data/code/my-fastrcnn/models/checkcode_vgg16/test.prototxt'
CAFFEMODEL = '/data/code/my-fastrcnn/output/default/train/checkcode_vgg16_fast_rcnn_iter_100000.caffemodel'
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


def label_images(src_img_path, dst_path):
    global PROTOTXT
    global CAFFEMODEL
    global CLASS_TUPLE
    imglist_file = src_img_path+'/'+'imglist.txt'
    if os.path.exists(imglist_file)==True:
        os.remove(imglist_file)
    #open file
    pfile = open(imglist_file, 'w')
    #load net
    caffe_net = fastrcnn.load_caffe_net(PROTOTXT, CAFFEMODEL, 1)
    imglist = get_file_list(src_img_path, 'jpg')
    num = len(imglist)
    for i in range(0,num):
        print 'process: %d'%(i+1)
        imgpath = src_img_path + '/' + imglist[i]
        if os.path.exists(imgpath)==False:
            continue
        cc_value = fastrcnn.recognize_checkcode_img(caffe_net, imgpath, CLASS_TUPLE)
        dpath = dst_path + '/' + cc_value['ccvalue'] + '.jpg'
        if os.path.exists(dpath)==True:
            dpath = dst_path + '/' + cc_value['ccvalue'] + '_' + random_string(6) + '.jpg'
        shutil.copyfile(imgpath, dpath)
        #char rect
        rects = cc_value['rects']
        pfile.write(imglist[i]+' ')
        pfile.write(cc_value['ccvalue']+' ')
        pfile.write(str(len(rects)))
        for elem in rects:
            pfile.write(' '+str(elem.get('xmin'))+' '+str(elem.get('ymin'))+' '+str(elem.get('xmax'))+' '+str(elem.get('ymax')))
        pfile.write('\n')
    pfile.close()


if __name__=='__main__':
    #label_images('/data/Images/checkcode/data/TestImgs2', '/data/Images/checkcode/data/TestImgs_label2')
    label_images('/data/Images/data_6/Images', '/data/Images/data_6/Label')
