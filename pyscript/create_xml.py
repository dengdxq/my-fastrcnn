#
import sys
import os
import dlib
from skimage import io
import numpy as np
import scipy.io as scio
from xml.dom import minidom
from xml.etree import ElementTree as etree
from xml.etree.ElementTree import Element, SubElement, ElementTree
from xml.dom import minidom


def get_file_list(train_list):
    files = open(train_list, 'r')
    filelist = []
    for text in files.readlines():
        strs = text.split('\n')
        if len(strs) != 2:
            print strs
            print 'ERROR: %s'%(text)
            continue 
        filelist.append(strs[0])
    files.close()
    return filelist


def convert_annotation_xml(filename, savepath):
    pfile = open(filename, 'r')
    for text in pfile.readlines():
        string = text.strip('\n')
        strs = string.split(' ')
        #print strs
        file_name = strs[0]
        label = strs[1]
        name_len = int(len(label))
        rect_num = int(strs[2])
        if name_len != rect_num:
            print "ERROR: %s"%(text)
            continue
        dict_rect = {}
        for i in range(rect_num):
            left = int(strs[4*i+3]) + 1
            top = int(strs[4*i+4]) + 1
            right = int(strs[4*i+5]) + 1
            bottom = int(strs[4*i+6]) + 1
            dict_rect[label[i]] = [left,top,right,bottom]
        #print dict_rect
        str = to_xml('checkcode', file_name, dict_rect)
        strs  =file_name.split('.')
        save_xml(str, savepath+"/"+strs[0]+'.xml')
        #print str
        #exit()

def to_xml(foldername, imgname, label_dict):
    annotation = Element('annotation')
    folder = SubElement(annotation, 'folder')
    folder.text = foldername
    filename = SubElement(annotation, 'filename')
    item = SubElement(filename, 'item')
    item.text =imgname
    object = SubElement(annotation, 'object')
    #num = len(label_list)
    #for i in range(num):
    for key,val in label_dict.items():
        name = SubElement(object, 'name')
        name.text = key
        bndbox = SubElement(object, 'bndbox')
        xmin = SubElement(bndbox, 'xmin')
        xmin.text = str(val[0])
        ymin = SubElement(bndbox, 'ymin')
        ymin.text = str(val[1])
        xmax = SubElement(bndbox, 'xmax')
        xmax.text = str(val[2])
        ymax = SubElement(bndbox, 'ymax')
        ymax.text = str(val[3])
    xml_string = etree.tostring(annotation)
    doc = minidom.parseString(xml_string)
    return doc.toprettyxml(indent = "\t", newl = "\n", encoding = "utf-8")


def save_xml(text, savepath):
    pfile = open(savepath, "w")
    pfile.write(text)
    pfile.close()


if __name__=='__main__':
    #test input
    #labelfile = '/Users/wangjj/Documents/download_code/imageset/imglist.txt'
    #save_path = '/Users/wangjj/Documents/download_code/imageset/xmls'
    #demo
    if len(sys.argv) < 3:
        print "ERROR: not enough arguments"
        print "Example:  python create_xml.py imglist.txt output_dir"
        exit()
    label_file = sys.argv[1]
    save_path = sys.argv[2]
    #print label_file
    #print save_path
    convert_annotation_xml(label_file, save_path)

    #for arg in sys.argv:
    #    print arg
    #print type(sys.argv)
