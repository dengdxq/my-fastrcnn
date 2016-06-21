import tornado.ioloop
import tornado.web
import urlparse
import fastrcnn
import _init_config
import json
import time
import random
import base64
import logging
import os
from urllib import unquote
import threading

CAFFE_NET = None
CLASS_TUPLE = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9')

def load_caffe_net():
	global CAFFE_NET
	CAFFE_NET = fastrcnn.load_caffe_net(_init_config.prototxt, _init_config.caffemodel, 1)
	save_img_path = ''
	img_num = 0

class MainHandler(tornado.web.RequestHandler):	
	logger = logging.getLogger('HttpMainHandler')
	def get(self):		
		global CAFFE_NET
		global CLASS_TUPLE
		param_dict = {}
		param_dict['tid'] = self.get_argument('tid', '')
		param_dict['data'] = self.get_argument('data', '')
		param_dict['type'] = self.get_argument('type', '')
		print param_dict['tid']
		#self.write(greeting)
		#self.write("Hello, world")
		if len(param_dict['tid'])==0:
			self.logger.info('The Params of tid is null!')
			self.write('parameter error!')
			return
		print '==========================================1==='
		if len(param_dict['type'])==0:
			self.logger.info('The Params of type is null!')
			self.write('parameter error!')
			return
		print '==========================================2==='
		if len(param_dict['data'])==0:
			self.logger.info('The Params of data is null!')
			self.write('parameter error!')
			return
		print '==========================================3==='
		self.logger.info('GET Params:%s'%(json.dumps(param_dict)))		
		self.logger.info('THREAD NAME = %s,num=%d'%(threading.currentThread().getName(), threading.activeCount()))
		#---save image---
		#file_num = self.get_file_number_in_dir(_init_config.img_save_dir)
		#if file_num==_init_config.img_max_num:
		print '==========================================4==='
		print _init_config.img_max_num
		if self.img_num ==_init_config.img_max_num:
		    self.make_dir(_init_config.img_save_dir)
		savepath = _init_config.img_save_dir + '/' + self.get_image_name() +'_' +param_dict['type']+'.jpg'
		print savepath
		self.logger.info('TID:%s; SAVE Image:%s'%(param_dict['tid'], savepath))        
		self.save_image(param_dict['data'], savepath)
		self.img_num += 1
		#---recognize---
		start_time = time.time()
		cc_value = fastrcnn.recognize_checkcode_img(CAFFE_NET, savepath, CLASS_TUPLE)['ccvalue']
		end_time = time.time()
		self.logger.info('TID:%s; recognize_checkcode_img take:%s sec'%(param_dict['tid'], str(end_time-start_time)))
		if cc_value == '':
		    cc_value = '{}'
		self.logger.info('TID:%s; RECOGNIZE Result:%s<=>%s'%(param_dict['tid'], savepath, cc_value))
		response_str = self.create_response(cc_value, param_dict['tid'])
		self.logger.info('TID:%s; RETURN String:%s'%(param_dict['tid'], response_str))
		self.write(response_str)

	def create_response(self, cc_value, tid):
		dict = {}
		dict['result'] = cc_value
		dict['tid'] = tid
		dict['image'] = ''
		response_str = json.dumps(dict)
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
	    stimestamp = stimestamp.replace('.', '_')
	    name = random.sample(alpha_list, 6)
	    name = ''.join(name)
	    fname = stimestamp+'_'+name
	    return fname

	def get_dir_name(self):
	    timestamp = time.time()
	    stimestamp = str(timestamp)
	    strs = stimestamp.split('.')
	    return strs[0]

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
	    return (path+'/'+dname)

	def get_file_list(self, path):
	    filelist = []
	    for root,dirs,files in os.walk(path):
	        filelist.extend(files)
	    return filelist




if __name__ == "__main__":
	load_caffe_net()
	print 'load caffe net complete!'
	application = tornado.web.Application([(r"/checkcode", MainHandler),])
	application.listen(8181)
	print 'checkcode recognize server start!'
	tornado.ioloop.IOLoop.instance().start()