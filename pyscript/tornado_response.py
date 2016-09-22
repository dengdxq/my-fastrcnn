#-*- coding:utf-8 –*-
import sys 
import tornado.ioloop
import tornado.web
import time
import json
import os
import traceback
import StringIO
import logging.config
import logging.handlers
import logging
import logconfig2


class MainHandler(tornado.web.RequestHandler):	
	logger = logging.getLogger('MainHandler')
	def get(self):
		param_dict = {}
		param_dict['tid'] = self.get_argument('tid', '')
		if len(param_dict['tid'])==0:
			self.logger.info('The Params of tid is null!')
			str_dict = {}
			str_dict['errcode'] = 101
			str_dict['errmsg'] = 'parameter error, loss tid!'
			self.write(json.dumps(str_dict))
			return
		self.logger.info('GET Params:%s'%(json.dumps(param_dict)))
		#
		self.logger.info('ERROR_TASKID=%s'%(param_dict['tid']))
		str_dict = {}
		str_dict['errcode'] = 0
		str_dict['errmsg'] = 'ok!'
		self.write(json.dumps(str_dict))


if __name__ == "__main__":
	port = sys.argv[1]
	thread_name = port
	logger = logging.getLogger('main')
	logger.info('restart isright server!')
	application = tornado.web.Application([(r"/report", MainHandler),])
	application.listen(int(port))
	logger.info('checkcode isright server start!')
	tornado.ioloop.IOLoop.instance().start()
	logger.info('checkcode isright server start complete!')
