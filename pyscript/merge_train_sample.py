#-*- coding:utf-8 –*-
import sys
import os
import random
import shutil

'''
合并多个图像目录文件,产生训练样本
'''

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

def get_random_string(length):
        alpha_list = ['9','8','7','6','5','4','3','2','1','0','z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a']
        name = random.sample(alpha_list, length)
        name = ''.join(name)
        return name

def copy_imagefiles(srcdir, name, dstdir):
    if os.path.exists(srcdir+'/'+name) == False:
        shutil.copyfile(srcdir+'/'+name, dstdir+'/'+name)
        return name
    newname = get_random_string(9)+'_'+name
    return newname


def merge_train_images(rootdir, dirlist, dstdir):
    pfile = open(dstdir+'/imglist.txt')
    for elem in dirlist:
        imgdir = rootdir+'/'+elem
        textlist = get_file_content_by_line(imgdir+'/'+'imglist.txt')
        for text in textlist:
            strs = text.split(' ')
            fname = copy_imagefiles(imgdir, strs[0], dstdir+'/Images')
            if cmp(fname, strs[0]) == 0:
                pfile.write(text + '\n')
                continue
            seq = ' '
            strs[0] = fname
            newstr = seq.join(strs)
            pfile.write(newstr+'\n')
    pfile.close()


if __name__=='__main__':
    img_path = '/data/'
    imgdir_list = ['a', 'b']
    out_path = ''
    merge_train_images('', imgdir_list, out_path)
