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


total_cnt = 0
right_cnt = 0 

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

def filter_files(srcpath, dstpath, files, tid_freq, day_timestamp, datestr, err_set):
	global total_cnt
	global right_cnt
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
		tid = strs[2]
		total_cnt += 1
		if err_set.has_key(tid) == False:
			shutil.copy(srcpath+'/'+elem, dstpath+'/'+datestr+'/'+elem)
			right_cnt += 1
			continue
		file_freq = tid_freq[tid]
		if err_set[tid]==1 and file_freq==1:
			#test_list.append(tid)
			#test_set.add(tid)
			continue
		if file_freq < err_set[tid]:
			print '=================='
			continue
		#test_set.add(tid)
		if file_dict.has_key(tid)==True:
			file_dict[tid].append(elem)
		else :
			file_dict[tid] = list()
			file_dict[tid].append(elem)
			#test_list.append(tid)
	#process more than one tid
	#print file_dict
	#print 'cnt=%d'%(cnt)
	#print 'cnt12=%d'%(cnt1+cnt2)
	#print 'cnt2=%d'%(cnt2)
	for tid,flist in file_dict.iteritems():
		flist.sort()
		flen = len(flist)
		num = err_set[tid]
		if num > flen:
			print '-------------'
			continue
		rest_files = []
		for i in list(xrange(num, flen)):
			rest_files.append(flist[i])		
		#print flist
		#print 'num=%d,flen=%d'%(num,flen)
		#print rest_files
		#print '-=-=-=-=-=-=-=-=-=-=-=-=-=-='
		for elem in rest_files:
			right_cnt += 1
			shutil.copy(srcpath+'/'+elem, dstpath+'/'+datestr+'/'+elem)

def get_tid_dict_from_files(filelist):
	tid_dict = {}
	for elem in filelist:
		strs = elem.split('_')
		if tid_dict.has_key(strs[2]):
			tid_dict[strs[2]] += 1
		else:
			tid_dict[strs[2]] = 1
	return tid_dict


def save_result(path):
	global total_cnt
	global right_cnt
	pfile = open(path, 'w')
	pfile.write('total='+str(total_cnt)+'\n')
	pfile.write('right='+str(right_cnt)+'\n')
	pfile.write('accurate='+str(1.0*right_cnt/total_cnt)+'\n')
	pfile.close()

if __name__ == '__main__':
	#global total_cnt
	#global right_cnt
	srcpath = '/data/checkcode/imgs'
	dstpath = '/data/checkcode/right_imgs'
	datestr = get_yesterday_date()#'2016-09-26'#get_yesterday_date()#get_local_date()
	day_timestamp = get_date_timestamp(datestr)
	dirlist = get_xdate_dir_list(srcpath, datestr)
	#print dirlist
	#print day_timestamp
	yesterdate = datestr#get_yesterday_date()
	#print yesterdate
	logfile = '/data/checkcode/logs/'+'checkcode_iserror.log.'+yesterdate
	if os.path.exists(logfile)==False:
		print '%s log file is no exist!'%(logfile)
		exit()
	#print logfile
	errtid = get_error_tids(logfile)	
	#print errtid
	#print '===errtaskid=='
	#print 'error tid = %d'%(len(errtid))
	#exit()
	for elem in dirlist:
		#print srcpath + '/'+elem
		files = get_file_list(srcpath + '/'+elem, 'jpg') 
		file_dict = get_tid_dict_from_files(files)
		#print len(files)
		filter_files(srcpath+'/'+elem, dstpath, files, file_dict, day_timestamp, datestr, errtid)
	#print 'rest err = %d'%(len(test_set))
	#print 'total=%d'%(total_cnt)
	#print 'right=%d'%(right_cnt)
	save_result('/data/checkcode/code/cnt_log/'+datestr+'_right.txt')	
