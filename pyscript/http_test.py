import requests
import threading
import time
import random
import os
import base64


class ImageSender(threading.Thread):
    files = []
    src_path = ''
    filenum = 0

    def __init__(self, num, interval):
        threading.Thread.__init__(self)
        self.thread_num = num
        self.interval = interval
        self.thread_stop = False
        self.src_path = ''
        self.files = self.get_file_list(self.src_path)
        self.filenum = len(self.files)
        print 'file num = %d'%(self.filenum)

    def run(self):
        while self.thread_stop==False:
            idx = random.randint(0, self.filenum)
            fpath = self.get_image_path(idx)
            if fpath == '':
                continue
            pfile = open(fpath, 'rb')
            text64 = base64.b64encode(pfile.read())
            pfile.close()
            self.url_request(text64)
            time.sleep(self.interval)

    def stop(self):
        self.thread_stop = True

    def get_file_list(self, path):
        filelist = []
        for root,dirs,files in os.walk(path):
            filelist.extend(files)
        return filelist

    def get_image_path(self, idx):
        path = self.src_path+'/'+self.files[idx]
        if os.path.exists(path)==True:
            return  path
        return ''

    def url_request(self, imgdata):
        url = ''
        params = {'tid':'2342sdfdsg', 'code':'asfaf', 'data': imgdata}
        r = requests.get(url, params)


def maintest():
    threadlist = []
    for i in range(5):
        threadlist[i] = ImageSender(i, 0.05)
        threadlist[i].start()
    time.sleep(30)


if __name__=='__main__':
    maintest()