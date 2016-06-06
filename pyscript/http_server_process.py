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


class HttpHandle(BaseHTTPRequestHandler):
    urlparam_str = ''
    urlparam_dict = None
    caffe_net = None
    class_tuple = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9')
    cc_value = ''
    response_str = ''
    logger = logging.getLogger('HttpHandle')

    def do_GET(self):
        self.logger.info('GET Params[src]:%s'%(self.path))
        parsed_path = urlparse.urlparse(self.path)
        self.parse_params(parsed_path.query)
        self.logger.info('GET Params[parse]:%s'%(json.dumps(self.urlparam_dict)))
        self.cc_value = fastrcnn.recognize_checkcode_img(self.caffe_net, '', self.class_tuple)
        if self.cc_value == None:
            self.cc_value = '{}'
        self.create_response()
        self.logger.info('RETURN String:%s'%(self.response_str))
        self.wfile.write(self.response_str)
        #---save image---
        savepath = _init_config.img_save_dir + '/' + self.get_image_name() +'_' +self.urlparam_dict['type']+'_'+self.cc_value+'.jpg'
        self.logger.info('SAVE Image:%s'%(savepath))
        self.save_image(savepath)

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

def start_server(url, port):
    http_server = HTTPServer((url, int(port)), HttpHandle)
    http_server.serve_forever()


if __name__ == '__main__':
    start_server('127.0.0.1', '8080')