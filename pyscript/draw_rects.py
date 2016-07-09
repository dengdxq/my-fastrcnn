#-*- coding:utf-8 –*-
import fastrcnn
import time
import cv2


def load_image(image_name):
    im = cv2.imread(image_name)
    h = im.shape[0]
    w = im.shape[1]
    if h >= 120:
        return im
    ratio = 1.0*w/h
    hh = 120
    ww = int(ratio*hh)
    img = cv2.resize(im, (ww,hh), interpolation=cv2.INTER_CUBIC)    
    return img


def draw_rect(srcpath, dstpath, rectlist):
	font=cv2.FONT_HERSHEY_SIMPLEX	
	img = load_image(srcpath)
	for rect in rectlist:
		lt_x = rect['xmin']
		lt_y = rect['ymin']
		rb_x = rect['xmax']
		rb_y = rect['ymax']
		print rect['char']
		print rect['score']
		cv2.putText(img,rect['char'],(lt_x,lt_y+10), font, 0.35, (255,0,0), 1)
		cv2.rectangle(img,(lt_x,lt_y),(rb_x,rb_y),(0,0,255), 1)
	cv2.imwrite(dstpath, img)

if __name__ == '__main__':
    prototxt = '/data/code/my-fastrcnn/models/checkcode_vgg16/test.prototxt'
    caffemodel = '/data/code/my-fastrcnn/output/default/train/checkcode_vgg16_fast_rcnn_iter_200000.caffemodel'
    #imgpath = '/data/Images/rootdir/aa_200/39.jpg'
    imgpath = '/data/aaa/checkImage/new_root_enlarge/2000/knim_b8E2G6NELowF00S00_gjj_fujian_42.jpg'#'/data/Images/rootdir_gjj/2000_f/aq6sdu_b8E2G6MJhoGP00310_gjj_shenyang_44.jpg'
    CLASS_TUPLE = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9')
    CAFFE_NET = fastrcnn.load_caffe_net(prototxt, caffemodel, 1)
    cc_value = fastrcnn.recognize_checkcode_img(CAFFE_NET, imgpath, CLASS_TUPLE)
    rectlist = cc_value['rects']
    print cc_value['ccvalue']
    draw_rect(imgpath, '/data/Images/res.jpg', rectlist)

