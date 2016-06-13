import fastrcnn
import time

prototxt = '/data/code/my-fastrcnn/models/checkcode_vgg16/test.prototxt'
caffemodel = '/data/code/my-fastrcnn/output/default/train/checkcode_vgg16_fast_rcnn_iter_10000.caffemodel'
imgpath = '/data/Images/checkcode/data/Images/x0qngSwj7OHYEVWgWVAc0TTer0hEwoOXGmFd0rRnVA8bHHrDsJm.jpg'
#matpath = '/data/Images/checkcode/data/ssbox/x0qngSwj7OHYEVWgWVAc0TTer0hEwoOXGmFd0rRnVA8bHHrDsJm_boxes.mat'
matpath = '/data/Images/checkcode/data/ssbox_matlab/x0qngSwj7OHYEVWgWVAc0TTer0hEwoOXGmFd0rRnVA8bHHrDsJm.mat'
savepath = '/data/code/my-fastrcnn/a.jpg'
caffe_net = fastrcnn.load_caffe_net(prototxt, caffemodel, 1)
class_tuple = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9')
start_time = time.time()
cc_value = fastrcnn.recognize_img(caffe_net, imgpath, matpath, class_tuple)
end_time = time.time()
print 'value of image: %s'%(cc_value)
print 'recognize checkcode img take:%s sec'%(str(end_time-start_time))
