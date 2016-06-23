#-*- coding:utf-8 –*-

import cv2
import os
import math

IMAGE_HEIGH = 60

def get_file_content_by_line(filepath):
    if os.path.exists(filepath) == False:
        print 'no exist: %s'%(filepath)
        return []
    pfile = open(filepath, 'r')
    textlist = []
    for text in pfile.readlines():
        textlist.append(text)
    pfile.close()
    return textlist



def resize_image(imgpath, nhei, savepath):
    img = cv2.imread(imgpath)
    width  = img.shape[1]
    height = img.shape[0]
    if height>=50:
        cv2.imwrite(savepath, img)
        return (1,1)
    wh = 1.0*width/height
    nheight = nhei
    nwidth = int(wh*nheight)
    res = cv2.resize(img,(nwidth,nheight),interpolation=cv2.INTER_CUBIC)
    #return res
    cv2.imwrite(savepath, res)
    wratio = 1.0*nwidth/width
    hratio = 1.0*nheight/height
    return (wratio,hratio)


def enlare_imgs(srcpath, dstpath):
    global IMAGE_HEIGH
    texts = get_file_content_by_line(srcpath+'/imglist.txt')
    pfile = open(dstpath+'/imglist.txt', 'w')
    for line in texts:
        strs = line.strip('\n').split(' ')
        ratio = resize_image(srcpath+'/'+strs[0], IMAGE_HEIGH, dstpath+'/'+strs[0])
        num = int(strs[2])*4/2
	idx = 0
        while idx < num:
            strs[3+idx*2] = str(int(round(int(strs[3+idx*2])*ratio[0])))
            strs[4+idx*2] = str(int(round(int(strs[4+idx*2])*ratio[1])))
	    idx += 1
        sep = ' '
        string = sep.join(strs)
        pfile.write(string+'\n')
    pfile.close()

#=====================

def get_fielist_jpg(dir):
    flist = []
    for root,dirs,files in os.walk(dir):
        for file in files:
            strs = file.split('.')
            if cmp(strs[1],'jpg')==0 or cmp(strs[1],'jpeg')==0:
                flist.append(file)
    return flist

def enlarge_imgs_without_txt(srcdir, dstdir):
    global IMAGE_HEIGH
    filelist = get_fielist_jpg(srcdir)
    for file in filelist:
        spath = srcdir + '/' + file
        dpath = dstdir + '/' + file
        resize_image(spath, IMAGE_HEIGH, dpath)


if __name__ == '__main__':
    '''
    #contain imglist.txt
    srcdir = '/data/Images/rootdir/src_aa200'
    dstdir = '/data/Images/rootdir/aa_200'
    enlare_imgs(srcdir, dstdir)
    '''
    #
    srcdir = '/data/Images/rootdir/src_aa200'
    dstdir = '/data/Images/rootdir/aa_200'
    enlarge_imgs_without_txt(srcdir, dstdir)
