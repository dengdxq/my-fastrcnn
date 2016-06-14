#-*- coding:utf-8 –*-
import fastrcnn
import time

#测试训练模型的正确率
#并且比较了matlab版的ss和dlib的ss之间的效果


IMAGE_DIR = '/data/Images/checkcode/data/Images'
SSBOX_DIR = '/data/Images/checkcode/data/ssbox'
CAFFE_NET = None
CLASS_TUPLE = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9')


def load_caffe_net(prototxt, caffemodel):
    global CAFFE_NET
    CAFFE_NET = fastrcnn.load_caffe_net(prototxt, caffemodel, 1)
    #return caffe_net

def load_annotation_file(filename):
    pfile = open(filename, 'r')
    line_no = 1
    cnt = 0
    cnt1 = 0
    cnt2 = 0
    cnt3 = 0
    cnt4 = 0
    for text in pfile.readlines():
        line_no += 1
        string = text.strip('\n')
        strs = string.split(' ')
        file_name = strs[0]
        label = strs[1]
        name_len = int(len(label))
        rect_num = int(strs[2])
        if name_len != rect_num:
            print "[ERROR]lineNo. %d: %s"%(line_no, text)
            continue
        cnt += 1
        ccvalue1 = get_checkcode_value_dlib(file_name)
        ccvalue2 = get_checkcode_value_matlab(file_name)
        flg1 = cmp(label, ccvalue1)
        flg2 = cmp(label, ccvalue2)
        flg3 = cmp(ccvalue1, ccvalue2)
        flg4 = cmp(ccvalue1.lower(), ccvalue2.lower())
        if flg1 == 0:
            cnt1 += 1
        if flg2 == 0:
            cnt2 += 1
        if flg3 == 0:
            cnt3 += 1
        if flg4 == 0:
            cnt4 += 1
	if flg4 != 0:
            print '%s != %s'%(ccvalue1,ccvalue2)
    result_dict = {}
    result_dict['total'] = cnt
    result_dict['ss_mat'] = cnt1
    result_dict['ss_dlib'] = cnt2
    result_dict['mat_dlib'] = cnt3
    return result_dict


#matlab
def get_checkcode_value_matlab(imagename):
    global CAFFE_NET
    global CLASS_TUPLE
    global SSBOX_DIR
    global IMAGE_DIR
    imgpath = IMAGE_DIR + '/' + imagename
    matpath = SSBOX_DIR + '/' + get_pure_filename(imagename) + '_boxes.mat'
    str = fastrcnn.recognize_img(CAFFE_NET, imgpath, matpath, CLASS_TUPLE)
    return str

def get_checkcode_value_dlib(imagename):
    global CAFFE_NET
    global CLASS_TUPLE
    global IMAGE_DIR
    imgpath = IMAGE_DIR + '/' + imagename
    str = fastrcnn.recognize_checkcode_img(CAFFE_NET, imgpath, CLASS_TUPLE)['ccvalue']
    return str

def get_pure_filename(filename):
    strs = filename.split('.')
    if len(strs)<2:
        return filename
    return strs[0]

if __name__ == '__main__': #53.4-979082-6230 ##1128253 = 149171  6575
    prototxt = '/data/code/my-fastrcnn/models/checkcode_vgg16/test.prototxt'
    caffemodel = '/data/code/my-fastrcnn/output/default/train/checkcode_vgg16_fast_rcnn_iter_180000.caffemodel'
    load_caffe_net(prototxt, caffemodel)
    imglist = '/data/Images/checkcode/imglist.txt'
    res = load_annotation_file(imglist)
    print res
    print 'Total image number is: %d'%(res['total'])
    print 'The accuracy of matlab ss is: %f'%(1.0*res['ss_mat']/res['total'])
    print 'The accuracy of dlib ss is: %f'%(1.0*res['ss_dlib']/res['total'])
    print 'The recognize result of matlab and dlib is %d'%(res['mat_dlib'])
