#-*- coding:utf-8 –*-

import cv2
import os
import math

IMAGE_HEIGH = 100

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
    wh = 1.0*width/height
    nheight = nhei
    nwidth = int(wh*nheight)
    res = cv2.resize(img,(nwidth,nheight),interpolation=cv2.INTER_CUBIC)
    #return res
    cv2.imwrite(savepath, res)
    return wh


def enlare_imgs(srcpath, dstpath):
    global IMAGE_HEIGH
    texts = get_file_content_by_line(srcpath+'/imglist.txt')
    pfile = open(dstpath+'/imglist.txt', 'w')
    for line in texts:
        strs = line.strip('\n').split(' ')
        ratio = resize_image(srcpath+'/'+strs[0], IMAGE_HEIGH, dstpath+'/'+strs[0])
        num = int(strs[2])*4
        for idx in range(num):
            strs[3+idx] = str(round(int(strs[3+idx])*ratio))
        sep = ' '
        string = sep.join(strs)
        pfile.write(string+'\n')
    pfile.close()

if __name__ == '__main__':
    srcdir = ''
    dstdir = ''
    enlare_imgs(srcdir, dstdir)