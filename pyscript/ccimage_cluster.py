#-*- coding:utf-8 –*-
import time
import shutil
import random
import os


def get_file_list(path, suffix):
    filelist = []
    for root,dirs,files in os.walk(path):
	for felem in files:
		strs = felem.split('.')
		if len(strs)!=2 or cmp(strs[1],suffix)!=0:
		    continue
	    	filelist.append(felem)
    return filelist


def process(filename, srcdir, dstdir):
	pfile = open(filename, 'r')
	type_dict = {}
	for text in pfile.readlines():
		linestr = text.strip('\n')
		#print linestr
		strs = linestr.split('/')
		if len(strs) < 2:
			print 'Error line: %s'%(linestr)
			continue
		namefields = strs[1].split('_')
		bank_type = namefields[1]
		#print namefields
		if os.path.exists(dstdir+'/'+bank_type)==False:
			os.mkdir(dstdir+'/'+bank_type)
		imgpath = srcdir + '/' + strs[1]
		dpath = dstdir + '/' + bank_type + '/' + strs[1]
		#shutil.copyfile(imgpath, dpath)
		if type_dict.has_key(bank_type) == True:
			type_dict[bank_type] += 1
		else :
			type_dict[bank_type] = 1
	print type_dict


def process2(srcdir, dstdir):
	fileset = get_file_list(srcdir, 'jpg')
	type_dict = {}
	for file in fileset:		
		namefields = file.split('_')
		bank_type = namefields[1]
		#print namefields
		if os.path.exists(dstdir+'/'+bank_type)==False:
			os.mkdir(dstdir+'/'+bank_type)
		imgpath = srcdir + '/' + file
		dpath = dstdir + '/' + bank_type + '/' + file
		shutil.copyfile(imgpath, dpath)
		if type_dict.has_key(bank_type) == True:
			type_dict[bank_type] += 1
		else :
			type_dict[bank_type] = 1
	print type_dict

def process_gjj(srcdir, dstdir):
	fileset = get_file_list(srcdir, 'jpg')
	type_dict = {}
	for file in fileset:		
		namefields = file.split('_')
		bank_type = namefields[3]
		#print namefields
		if os.path.exists(dstdir+'/'+bank_type)==False:
			os.mkdir(dstdir+'/'+bank_type)
		imgpath = srcdir + '/' + file
		dpath = dstdir + '/' + bank_type + '/' + file
		shutil.copyfile(imgpath, dpath)
		if type_dict.has_key(bank_type) == True:
			type_dict[bank_type] += 1
		else :
			type_dict[bank_type] = 1
	print type_dict


if __name__ == '__main__':
	wrong_file = '/home/jiayuan/Downloads/wrongList.html.Rename'
	src_dir = '/data/aaa/checkImage/20160614'
	dst_dir = '/data/aaa/checkImage/gjj'
	#process(wrong_file, src_dir, dst_dir)
	#process2(src_dir, dst_dir)
	process_gjj(src_dir, dst_dir)