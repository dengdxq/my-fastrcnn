#-*- coding:utf-8 –*-

import cv2
import os
import math

IMAGE_HEIGH = 120#60

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
    if height>=IMAGE_HEIGH:
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
            x = int(strs[3+idx*2])
            y = int(strs[4+idx*2])
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            strs[3+idx*2] = str(int(round(x*ratio[0])))
            strs[4+idx*2] = str(int(round(y*ratio[1])))
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
    if os.path.exists(dstdir)==False:
        os.mkdir(dstdir)
    filelist = get_fielist_jpg(srcdir)
    for file in filelist:
        spath = srcdir + '/' + file
        dpath = dstdir + '/' + file
        resize_image(spath, IMAGE_HEIGH, dpath)



def get_dir_list(path):
    dirlist = []
    for root,dirs,files in os.walk(path):
        if len(dirs) != 0:
            dirlist.extend(dirs)
    return dirlist


if __name__ == '__main__':
    '''
    #contain imglist.txt
    srcdir = '/data/Images/rootdir/all'
    dstdir = '/data/Images/rootdir/en_all'
    enlare_imgs(srcdir, dstdir)
    '''
    #
    '''
    srcdir = '/data/Images/rootdir1/src_icbc1_500'
    dstdir = '/data/Images/rootdir1/icbc1_500'
    enlarge_imgs_without_txt(srcdir, dstdir)
    '''
    #
    #'''
    srcdir = '/data/aaa/checkImage/new_root'
    dstdir = '/data/aaa/checkImage/new_root_enlarge'
    dirlist = get_dir_list(srcdir)
    for elem in dirlist:
        enlarge_imgs_without_txt(srcdir+'/'+elem, dstdir+'/'+elem)
    #'''
