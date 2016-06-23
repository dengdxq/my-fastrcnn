import requests
import threading
import time
import random
import os
import base64
from urllib import quote,unquote

class ImageSender(threading.Thread):
    files = []
    src_path = ''
    filenum = 0

    def __init__(self, num, interval):
        threading.Thread.__init__(self)
        self.thread_num = num
        self.interval = interval
        self.thread_stop = False
        self.src_path = '/data/Images/checkcode/data/Images'
        self.files = self.get_file_list(self.src_path)
        self.filenum = len(self.files)
        print 'file num = %d'%(self.filenum)

    def run(self):
        while self.thread_stop==False:
            idx = random.randint(0, self.filenum)
            print 'idx=%d'%idx
            fpath = self.get_image_path(idx)
            if fpath == '':
                continue
            pfile = open(fpath, 'r')
            text64 = base64.b64encode(pfile.read())
            #text64 = base64.b64encode('abcdefg123')
            #print 'img size = %d'%(len(text64))
            pfile.close()
            #self.url_request(quote(text64))
            self.url_request(text64)
            time.sleep(self.interval)


    def get_tid(self):
        alpha_list = ['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a']
        name = random.sample(alpha_list, 12)
	name = ''.join(name)
        return name

    def stop(self):
        self.thread_stop = True

    def get_file_list(self, path):
        filelist = []
        print path
        for root,dirs,files in os.walk(path):
            filelist.extend(files)
        return filelist

    def get_image_path(self, idx):
        path = self.src_path+'/'+self.files[idx]
        if os.path.exists(path)==True:
            return path
        return ''

    def url_request(self, imgdata):
        #
        #print 'img size = %d'%(len(imgdata))
        #print imgdata
        #
        url = 'http://127.0.0.1:8181/checkcode'
        tid = self.get_tid()+'_'+str(self.thread_num)
        param = {'tid':tid, 'type':'TEST', 'data': imgdata}
        r = requests.get(url, params=param)
        #r = requests.get('http://127.0.0.1:8180/checkcode?tid=asdfasdff&type=CCCCC&data='+imgdata)
        #print '====================='
        print 'thread-%d send image'%(self.thread_num)
        #print r.url
        #print 'url = %s'%(r.text)

def maintest(thnum):
    threadlist = []
    for i in range(thnum):
        threadlist.append(ImageSender(i, 0.5))
    for i in range(thnum):
        threadlist[i].start()
    time.sleep(30)


if __name__=='__main__':
    maintest(10)
