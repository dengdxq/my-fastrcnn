#-*- coding:utf-8 –*-
import sys
import matplotlib 
matplotlib.use('Agg') 
import tornado.ioloop
import tornado.web
import urlparse
import fastrcnn
import _init_config
import json
import time
import random
import base64
#import logging
import os
import traceback
import StringIO
from urllib import unquote
import logging.config
import logging.handlers
import logging
#import threading


thread_name = ''
CAFFE_NET = None
CLASS_TUPLE = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9')
img_num = 0
save_image_path = ''

def load_caffe_net():
	global CAFFE_NET
	CAFFE_NET = fastrcnn.load_caffe_net(_init_config.prototxt, _init_config.caffemodel, 1)
	

class MainHandler(tornado.web.RequestHandler):
	logger = logging.getLogger('HttpMainHandler')

	#def initialize(self, thname):
	#	self.thread_name = thname

	def get(self):		
		global img_num
		global save_image_path
		global CAFFE_NET
		global CLASS_TUPLE
		param_dict = {}
		param_dict['tid'] = self.get_argument('tid', '')
		param_dict['data'] = self.get_argument('data', '')
		param_dict['type'] = self.get_argument('type', '')
		param_dict['isalphabet'] = self.get_argument('isalphabet', '')
		#print param_dict['tid']
		#self.write(greeting)
		#self.write("Hello, world")
		if len(param_dict['tid'])==0:
			self.logger.info('The Params of tid is null!')
			str_dict = {}
			str_dict['errcode'] = 101
			str_dict['errmsg'] = 'parameter error, loss tid!'
			self.write(json.dumps(str_dict))
			return		
		if len(param_dict['type'])==0:
			self.logger.info('The Params of type is null!')
			str_dict = {}
			str_dict['errcode'] = 102
			str_dict['errmsg'] = 'parameter error, loss type!'
			self.write(json.dumps(str_dict))
			return
		if len(param_dict['data'])==0:
			self.logger.info('The Params of data is null!')
			str_dict = {}
			str_dict['errcode'] = 103
			str_dict['errmsg'] = 'parameter error, loss data!'
			self.write(json.dumps(str_dict))
			return
		self.logger.info('GET Params:%s'%(json.dumps(param_dict)))		
		#self.logger.info('THREAD NAME = %s,num=%d'%(threading.currentThread().getName(), threading.activeCount()))
		#---save image---
		#file_num = self.get_file_number_in_dir(_init_config.img_save_dir)
		#if file_num==_init_config.img_max_num:
		#print '%s=%d'%(save_image_path,img_num)
		flg = self.is_recognized(param_dict['type'])
		if flg == 1:
			self.logger.info('type=%s in no recoginze list!'%(param_dict['type']))
			return
		if img_num==_init_config.img_max_num or img_num==0 or os.path.exists(save_image_path)==False:
			save_image_path = self.make_dir(_init_config.img_save_dir)
			img_num = 0
		#print param_dict['tid']
		savepath = save_image_path + '/' + self.get_image_name() +'_'+param_dict['tid']+'_'+param_dict['type']+'.jpg'
		self.logger.info('TID:%s; SAVE Image:%s'%(param_dict['tid'], savepath))
		self.save_image(param_dict['data'], savepath)
		img_num += 1
		#---recognize---
		start_time = time.time()
		try:
			cc_value = fastrcnn.recognize_checkcode_img(CAFFE_NET, savepath, CLASS_TUPLE)['ccvalue']
		except :
			fp = StringIO.StringIO()
			traceback.print_exc(file=fp)
			message = fp.getvalue()
			self.logger.info('[ERROR-start]: TID:%s, errorinfo:\n%s\n[ERROR-end]'%(param_dict['tid'], message))
		end_time = time.time()
		cc_result = '-1'
		if cc_value != '':
			cc_result = cc_value 
		self.logger.info('TID:%s; recognize_checkcode_img take:%s sec'%(param_dict['tid'], str(end_time-start_time)))
		self.logger.info('TID:%s; RECOGNIZE Result:%s<=>%s'%(param_dict['tid'], savepath, cc_result))
		#
		#'''
		if len(param_dict['isalphabet'])!=0:
			res = self.is_string_valid(cc_result, param_dict['isalphabet'])
			if res==1: #not fit the fitness
				self.logger.info('TID:%s; The RECOGNIZE Result don\'t satisfy the checkcode type!'%(param_dict['tid']))
				response_str = self.create_response('', param_dict['tid'])
				self.write(response_str)
				return
		#'''
		#
		response_str = self.create_response(cc_value, param_dict['tid'])
		self.logger.info('TID:%s; RETURN String:%s'%(param_dict['tid'], response_str))
		self.write(response_str)

	def create_response(self, cc_value, tid):
		str_dict = {}
		str_dict['result'] = cc_value
		str_dict['tid'] = tid
		str_dict['image'] = ''
		response_str = json.dumps(str_dict)
		return response_str

	def save_image(self, imgdata, savepath):
		base64str = imgdata
		string = unquote(base64str)
		string = base64.b64decode(string)
		file = open(savepath, 'wb')
		file.write(string)
		file.close()

	def get_image_name(self):
	    alpha_list = ['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a']
	    timestamp = time.time()
	    stimestamp = str(timestamp)
	    #stimestamp = stimestamp.replace('.', '_')
	    stimestamp = stimestamp.split('.')[0]
	    name = random.sample(alpha_list, 6)
	    name = ''.join(name)
	    fname = stimestamp+'_'+name
	    return fname

	def get_dir_name(self):
		global thread_name
		alpha_list = ['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a']
		randstr = random.sample(alpha_list, 6)
		randstr = ''.join(randstr)
		timestamp = time.time()
		#stimestamp = str(timestamp)
	    #strs = stimestamp.split('.')
	    #imeStr=time.strftime("%Y-%m-%d %H:%M:%S", ltime)
	    #return strs[0]
	    #format date
		ft = time.localtime(timestamp)
		string = time.strftime('%Y-%m-%d_%H-%M-%S', ft)
		return (string+'_'+thread_name)


	def get_file_number_in_dir(self, path):
		count = 0
		for root,dirs,files in os.walk(path):
		    count += len(files)
		return count

	def make_dir(self, path):
	    dname = self.get_dir_name()	    
	    while True:
	        if os.path.exists(path+'/'+dname)==False:
	            break
	        dname = self.get_dir_name()
	    os.mkdir(path+'/'+dname)
	    return (path+'/'+dname)

	def get_file_list(self, path):
	    filelist = []
	    for root,dirs,files in os.walk(path):
	        filelist.extend(files)
	    return filelist

	def is_recognized(self, cctype):
		if cctype in _init_config.type_black_list:
			return 1
		return 0

	def is_string_valid(self, string, cctype):
		res = self.is_digit_alphabet(string)
		if str(res)==cctype:
			return 0
		return 1

	def is_digit_alphabet(self, string):
		if string.isdigit():
			return 0
		elif string.isalpha():
			return 1
		return 2

def log_config(log_file_name):
	logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            # 当达到10MB时分割日志
            #'maxBytes': 1024 * 1024 * 10,
            'maxBytes': _init_config.log_file_size,
            # 最多保留50份文件
            'backupCount': _init_config.log_file_max_num,
            # If delay is true,
            # then file opening is deferred until the first call to emit().
            'delay': True,
            #'filename': _init_config.log_file+'/'+_init_config.log_file_name,
            'filename': _init_config.log_file+'/'+log_file_name,
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    }
})

if __name__ == "__main__":
	#global thread_name
	port = sys.argv[1]
	log_name = sys.argv[2]
	thread_name = port
	#
	log_config(log_name)
	#
	logger = logging.getLogger('main')
	logger.info('restart recognize server!')
	load_caffe_net()
	logger.info('load caffe net complete!')
	application = tornado.web.Application([(r"/checkcode", MainHandler),])
	application.listen(int(port))
	logger.info('checkcode recognize server start!')
	tornado.ioloop.IOLoop.instance().start()
	logger.info('checkcode recognize server complete!')
