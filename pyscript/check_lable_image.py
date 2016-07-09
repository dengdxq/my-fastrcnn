#-*- coding:utf-8 –*-
import time
import random
import os
import base64
from urllib import quote,unquote


'''
nchar == 0 or nchar==-1
表示不输入字符个数,默认以标定的字符合数为主
'''
def check_lable_file(filepath, charnum):
	pfile = open(filepath, 'r')
	lineno = 1
	for text in pfile.readlines():
		text = text.strip('\n')
		strs = text.split(' ')
		#print strs
		len1 = len(strs[1])
		len2 = int(strs[2])
		nrect = get_rect_num(strs)
		nchar = len1
		if charnum==0 or charnum==-1:
			nchar = len1
		if len1 != nchar:
			print 'The number of label-text is not equal to actual char number; lineNo:%d,filename:%s,lablename:%s'%(lineno, strs[0], strs[1])
		elif len2 != nchar:
			print 'The number of label-rect is not equal to actual char number; lineNo:%d,filename:%s,lablename:%s'%(lineno, strs[0], strs[1])
		elif len1 != len2:
			print 'The number of label-text and label-rect is not equal; lineNo:%d,filename:%s,lablename:%s'%(lineno, strs[0], strs[1])
		elif len2 != nrect:
			print 'The number of label-rect is not equal to actual rect number; lineNo:%d,filename:%s,lablename:%s'%(lineno, strs[0], strs[1])
		lineno += 1
	pfile.close()


def check_duplicate_line(filepath):
	pfile = open(filepath, 'r')
	dict = {}
	for text in pfile.readlines():
		text = text.strip('\n')
		strs = text.split(' ')
		if dict.has_key(strs[0])==True:
			dict[strs[0]] += 1
		else:
			dict[strs[0]] = 1
	pfile.close()
	for k in dict.keys():
		if dict[k] >= 2:
			print k


def get_rect_num(strs):
	num = len(strs)
	n = (num-3)/4.0
	return n

if __name__ == '__main__':
	#检查训练样本文件的正确性
	rootdir = '/data/Images/rootdir_gjj'
	#dirdict = {'163_999':6, 'ccb0_200':5, 'ccb1_200':5, 'ccb2_200':5, 'ccb3_200':5, 'cgb_200':4, 'ecitic_100':4, 'ecitic_200':4, 'spdb_247':6}
	dirdict = {'Images':-1}
        for (k,v) in dirdict.items():
	    print 'DIR:%s'%(k)
	    check_lable_file(rootdir+'/'+k+'/imglist.txt', -1)
	    print '----------------------------------------'
	#检查是否有重复的行
	#check_duplicate_line('/data/Images/checkcode/imglist.txt')
