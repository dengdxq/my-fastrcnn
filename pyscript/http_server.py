#-*- coding:utf-8 –*-

import socket
import base64
from urllib import unquote
import fastrcnn
import _init_config
import time
import random


def parse_url(request_str):
    if len(request_str)==0:
        return '' 
    strs = request_str.split('\n')
    url = ""
    length = len(strs)
    for i in range(length):
        if strs[i].find("GET") >=0:
            url = strs[i].split(' ')[1]
            break
    return url

def parse_params(url_str):
     if len(url_str)==0:
         return {}
     url_params = url_str.strip('\r\n').split('?')
     params = {}
     strs = url_params[1].split('&')
     length = len(strs)
     for i in range(length):
         param = strs[i].split('=')
         if len(param)<2:
             continue
         params[param[0]] = param[1]
     return params

def process_(param_dic):
    if param_dic.has_key('data'):
        save_img('', param_dic['data'])
    if param_dic.has_key('code'):
        pass

def save_img(savepath, base64str):
    str = unquote(base64str)
    str = base64.b64decode(str)
    file=open(savepath, 'wb')
    file.write(str)
    file.close()

def create_imgname():
    alpha_list = ['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a']
    #_init_config.img_save_dir
    timestamp = time.time()
    stimestamp = str(timestamp)
    stimestamp = stimestamp.replace('.', '_')
    name = random.sample(alpha_list, 6)
    name = ''.join(name)
    fname = stimestamp+'_'+name
    return fname

def http_server():
    HOST, PORT = '', 8888
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(1)
    #fast rcnn info
    class_tuple = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9')
    net = fastrcnn.load_caffe_net(_init_config.prototxt, _init_config.caffemodel, 1)
    print '------------------------------------------------------------------------------'
    #
    print 'Serving HTTP on port %s ...' % PORT
    while True:
        client_connection, client_address = listen_socket.accept()
        request = client_connection.recv(1024*3)
        url = parse_url(request)
        params = parse_params(url)
        print params
        if len(params) != 0:
            #print params            
            savepath = _init_config.img_save_dir + '/' + create_imgname() +'_' +params['type']+'.jpg'
            save_img(savepath, params['data'])
            
            boxes = fastrcnn.get_selective_search_boxes(savepath)
            str = fastrcnn.recognize_img(net, savepath, boxes, class_tuple)
            print "The result = %s"%(str)
            
        #http_response = """HTTP/1.1 200 OKHello, World!"""
        http_response = """
        HTTP/1.1 200 OK
        Hello, World!
        asfafasfafaff
        """
        client_connection.send(http_response)
        client_connection.close()

if __name__=='__main__':
    http_server()
    #print create_imgname()
    '''
    HOST, PORT = '', 8888
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(1)
    print 'Serving HTTP on port %s ...' % PORT
    while True:
        client_connection, client_address = listen_socket.accept()
        request = client_connection.recv(1024)
        url = parse_url(request)
        params = parse_params(url)
        #if len(params)==0:
        #    continue
        print params

        http_response = """
        HTTP/1.1 200 OK

        Hello, World!
        """
        client_connection.sendall(http_response)
        client_connection.close()
    '''
