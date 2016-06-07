from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import urlparse
import fastrcnn
import _init_config
import json
import time
import random
import base64
import logging
from urllib import unquote
import os


class HttpHandle(BaseHTTPRequestHandler):
    urlparam_str = ''
    urlparam_dict = None
    caffe_net = None
    class_tuple = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9')
    cc_value = ''
    response_str = ''
    logger = logging.getLogger('HttpHandle')
    caffe_net = fastrcnn.load_caffe_net(_init_config.prototxt, _init_config.caffemodel, 1)

    def do_GET(self):
        self.logger.info('GET Params[src]:%s'%(self.path))
        parsed_path = urlparse.urlparse(self.path)
        self.urlparam_str = parsed_path.query
        self.urlparam_dict = self.parse_params()
        self.logger.info('GET Params[parse]:%s'%(json.dumps(self.urlparam_dict)))
        #---save image---
        file_num = self.get_file_number_in_dir(_init_config.img_save_dir)
        if file_num==_init_config.img_max_num:
            self.make_dir(_init_config.img_save_dir)
        savepath = _init_config.img_save_dir + '/' + self.get_image_name() +'_' +self.urlparam_dict['type']+'.jpg'
        self.logger.info('SAVE Image:%s'%(savepath))        
        self.save_image(savepath)
        #---recognize---
        self.cc_value = fastrcnn.recognize_checkcode_img(self.caffe_net, savepath, self.class_tuple)
        if self.cc_value == None:
            self.cc_value = '{}'
        self.logger.info('RECOGNIZE Result:%s<=>%s'%(savepath, self.cc_value))
        self.create_response()
        self.logger.info('RETURN String:%s'%(self.response_str))
        self.wfile.write(self.response_str)
        

    def parse_params(self):
        dict = {}
        strs = self.urlparam_str.split('&')
        for elem in strs:
            keyvalue = elem.split('=')
            if len(keyvalue) < 2:
                continue
            dict[keyvalue[0]] = keyvalue[1]
        return dict

    def init_server(self):
        self.caffe_net = fastrcnn.load_caffe_net(_init_config.prototxt, _init_config.caffemodel, 1)

    def create_response(self):
        dict = {}
        dict['result'] = self.cc_value
        dict['tid'] = self.urlparam_dict['tid']
        dict['image'] = ''
        self.response_str = json.dumps(dict)

    def save_image(self, savepath):
        base64str = self.urlparam_dict['data']
        str = unquote(base64str)
        str = base64.b64decode(str)
        file=open(savepath, 'wb')
        file.write(str)
        file.close()

    def get_image_name(self):
        alpha_list = ['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a']
        #_init_config.img_save_dir
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

    def get_file_list(self, path):
        filelist = []
        for root,dirs,files in os.walk(path):
            filelist.extend(files)
        return filelist



def start_server(url, port):
    http_server = HTTPServer((url, int(port)), HttpHandle)
    http_server.serve_forever()


if __name__ == '__main__':
    start_server('127.0.0.1', '8080')