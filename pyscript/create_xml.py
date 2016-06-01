#-*- coding:utf-8 –*-
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


def convert_annotation_xml(filename, savepath):
    pfile = open(filename, 'r')
    trainname_list = []
    error_lsit = []
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
            error_lsit.append(text)
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
        trainname_list.append(strs[0])
        #print str
        #exit()
    write_to_file(error_lsit)
    return trainname_list

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

def dump_train_txt(trainlist, savepath):
    listlen = len(train_list)
    if listlen==0:
        return
    pfile = open(savepath, "w")
    for i in range(listlen):
        pfile.write(train_list[i]+'\n')
    pfile.close()

def write_to_file(text_list):
    listlen = len(text_list)
    if listlen==0:
        return
    pfile = open("invalid_.txt", "w")
    for i in range(listlen):
        pfile.write(text_list[i]+'\n')
    pfile.close()

if __name__=='__main__':
    #test input
    #labelfile = '/Users/wangjj/Documents/download_code/imageset/imglist.txt'
    #save_path = '/Users/wangjj/Documents/download_code/imageset/xmls'
    #demo
    print sys.argv
    if len(sys.argv) < 4:
        print "ERROR: not enough arguments"
        print "Example:  python create_xml.py imglist.txt output_dir"
        print "示例: python create_xml.py 标注的文件列表 输出xml格式的ground_truth目录 输出train.txt列表文件"
        exit()
    label_file = sys.argv[1]
    save_path = sys.argv[2]
    train_savepath = sys.argv[3]
    #print label_file
    #print save_path
    train_list = convert_annotation_xml(label_file, save_path)
    dump_train_txt(train_list, train_savepath)
    #for arg in sys.argv:
    #    print arg
    #print type(sys.argv)
