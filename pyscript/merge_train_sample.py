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
    #print '(%s)(%s)(%s)'%(srcdir+'/'+name,name,dstdir+'/'+name)
    if os.path.exists(dstdir+'/'+name) == False:        
        shutil.copyfile(srcdir+'/'+name, dstdir+'/'+name)
        return name
    newname = get_random_string(9)+'_'+name
    shutil.copyfile(srcdir+'/'+name, dstdir+'/'+newname)
    return newname


def merge_train_images(rootdir, dirlist, dstdir):
    pfile = open(dstdir+'/imglist.txt', 'w')
    for elem in dirlist:
        imgdir = rootdir+'/'+elem
        textlist = get_file_content_by_line(imgdir+'/'+'imglist.txt')
        for text in textlist:
            strs = text.strip('\n').split(' ')
            fname = copy_imagefiles(imgdir, strs[0], dstdir+'/Images')
            if cmp(fname, strs[0]) == 0:
                pfile.write(text)
                continue
            seq = ' '
            strs[0] = fname
            newstr = seq.join(strs)
            pfile.write(newstr+'\n')
    pfile.close()


if __name__=='__main__':
    rootpath = '/data/Images/rootdir_gjj'
    #imgdir_list = ['163_999', 'ecitic_100', 'ecitic_200', 'ccb0_200', 'ccb1_200', 'ccb2_200', 'ccb3_200', 'cgb_200', 'spdb_247']
    imgdir_list = ['0_f', '500_f', '1000_f', '1500_f', '2000_f', '2500_f', '3000_f', '3500_f', '4000_f']
    out_path = '/data/Images/checkcode/data'
    merge_train_images(rootpath, imgdir_list, out_path)
