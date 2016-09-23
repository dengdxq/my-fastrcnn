#-*- coding:utf-8 –*-
import sys 
import tornado.ioloop
import tornado.web
import time
import json
import os
import traceback
import StringIO
import shutil
import datetime

def get_file_list(path, suffix):
    filelist = []
    for root,dirs,files in os.walk(path):
        for felem in files:
            strs = felem.split('.')
            num = len(strs)
            if cmp(strs[num-1],suffix)!=0:
                continue
            filelist.append(felem)
    return filelist

def get_xdate_dir_list(imgdir, datestr):
		dirnamelist = get_dirs(imgdir)
		dirnamelist.sort()
		dirlist = []
		for elem in dirnamelist:
			if datestr not in elem:
				continue
			dirlist.append(elem)
		idx = dirnamelist.index(dirlist[0])
		if idx > 0:
			dirlist.append(dirnamelist[idx-1])
		dirlist.sort()
		return dirlist

def get_xday_files(imgdir, dirlist, start_t, end_t):
	for elem in dirlist:
		files = self.get_all_files()


def get_dirs(path):
	dirlist = []
	tmplist = os.listdir(path) 
	for elem in tmplist:
		if os.path.isdir(path+'/'+elem)==False:
			continue
		dirlist.append(elem)
	return dirlist

def get_local_date():
	t = time.localtime()
	date = time.strftime('%Y-%m-%d', t)
	return date


def get_yesterday_date():
	now = datetime.datetime.now()
	d2 = now - datetime.timedelta(days=1)
	date = d2.strftime("%Y-%m-%d")
	return date

def get_date_timestamp(datestr):
	start_str = datestr +  ' ' + '0-0-0'
	end_str = datestr +  ' ' + '23-59-59'
	timearray = time.strptime(start_str, "%Y-%m-%d %H-%M-%S")
	start = int(time.mktime(timearray))
	timearray = time.strptime(end_str, "%Y-%m-%d %H-%M-%S")
	end = int(time.mktime(timearray))
	return {'start':start, 'end':end}

def get_local_time():
	t = time.localtime()
	date = time.strftime('%Y-%m-%d', t)
	return date

def get_error_tids(filepath):
	err_tid_set = {} 
	pfile = open(filepath, 'r')
	for line in pfile.readlines():
		if 'ERROR_TASKID' not in line:
			continue
		strs = line.strip('\n').split('=')
		if len(strs) < 2:
			continue
		tid = strs[1]
		if err_tid_set.has_key(tid):
			err_tid_set[tid] += 1
		else:
			err_tid_set[tid] = 1
	pfile.close()
	return err_tid_set

def filter_files(srcpath, dstpath, files, day_timestamp, datestr, err_set):
	if os.path.exists(dstpath+'/'+datestr) == False:
		os.mkdir(dstpath+'/'+datestr)
	dpath = dstpath+'/'+datestr
	start = day_timestamp['start']
	end = day_timestamp['end']
	file_dict = {}
	#process single tid
	for elem in files:
		strs = elem.split('_')
		timestamp = int(strs[0])
		if timestamp<start or timestamp>end:
			continue	
		if err_set.has_key(str[2]) and err_set[str[2]]==1:
			continue
		elif err_set.has_key(str[2]) and err_set[str[2]]>1 :
			if file_dict.has_key(str[2])==True:
				file_dict[str[2]].append(elem)
			else :
				file_dict[str[2]] = list()
				file_dict[str[2]].append(elem)
			continue
		#if strs[2] in err_set:
		#	print elem
		#	continue
		shutil.copy(srcpath+'/'+elem, dstpath+'/'+datestr+'/'+elem)
		#print srcpath+'/'+elem
		#print dstpath+'/'+datestr+'/'+elem
	#process more than one tid
	for k,v in file_dict.iteritems():
		tid = k
		flist = v
		flist.sort()
		flen = len(flist)
		num = err_set[tid]
		if num >= flen:
			continue
		rest_files = []
		for i in list(xrange(num, flen)):
			rest_files.append(flist[i])		
		for elem in rest_files:
			shutil.copy(srcpath+'/'+elem, dstpath+'/'+datestr+'/'+elem)

if __name__ == '__main__':
	srcpath = '/data/checkcode/imgs'
	dstpath = '/data/checkcode/right_imgs'
	datestr = get_yesterday_date()#get_local_date()
	day_timestamp = get_date_timestamp(datestr)
	dirlist = get_xdate_dir_list(srcpath, datestr)
	print dirlist
	print day_timestamp
	yesterdate = get_yesterday_date()
	print yesterdate
	logfile = '/data/checkcode/logs/'+'checkcode_iserror.log.'+yesterdate
	if os.path.exists(logfile)==False:
		print '%s log file is no exist!'%(logfile)
		exit()
	errtid = get_error_tids(logfile)	
	#print '===errtaskid=='
	#print errtid
	#exit()
	for elem in dirlist:
		#print srcpath + '/'+elem
		files = get_file_list(srcpath + '/'+elem, 'jpg') 
		#print len(files)
		filter_files(srcpath+'/'+elem, dstpath, files, day_timestamp, datestr, errtid)
