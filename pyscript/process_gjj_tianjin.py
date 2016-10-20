#-*- coding:utf-8 -*-
import sys
import os
import cv2
import numpy as np
from PIL import Image
import pytesseract


def getHistThreshold(img):
	if img is None:
		return None
	hist = np.zeros(256).reshape(1,256)
	for row in img:
		for col in row:
			hist[0][col] += 1
	#print hist
	idxArr = np.argsort(-hist)
	return {'th1':idxArr[0][1], 'th2':idxArr[0][2]}

def getBinaryImg(imgpath):
	img = cv2.imread(imgpath, 0)
	#cv2.imwrite('result1.jpg', img)
	if img is None:
		return None
	ths = getHistThreshold(img)
	#print ths
	dstimg = np.zeros(img.shape, np.uint8)
	#cv2.imwrite('result2.jpg', dstimg)
	extractPixels(img, dstimg, ths['th1'])
	extractPixels(img, dstimg, ths['th2'])
	#cv2.imwrite('result3.jpg', dstimg)
	return 255-dstimg


def extractPixels(srcimg, dstimg, th):
	if srcimg is None or dstimg is None:
		return None
	height = srcimg.shape[0]
	width = srcimg.shape[1]
	for i in xrange(0,height):
		for j in xrange(0,width):
			if srcimg[i][j] == th:
				dstimg[i][j] = 255

def getResult(img):
	if img is None:
		return ''
	pilImg = Image.fromarray(img)
	#print type(pilImg)
	string = pytesseract.image_to_string(pilImg, lang='eng', config='-psm 7')
	#print string
	strlen = len(string)
	#print strlen
	if strlen < 5:
		return ''
	char1 = 0
	if string[0]>='0' and string[0]<='9':
		char1 = int(string[0])
	ope = string[1]
	char2 = 0
	if string[2]>='0' and string[2]<='9':
		char2 = int(string[2])
	if ope=='+':
		return char1+char2
	if ope=='-':
		return char1-char2
	if ope=='*':
		return char1*char2
	return ''


def recognize_gjj_tianjin(path):
	binImg = getBinaryImg(path)
	#cv2.imwrite('result.jpg', binImg)
	#print 'asdfaasfa==2'
	#print binImg
	result = getResult(binImg)
	#print 'asdfaasfa==3'
	res = {}
	res['ccvalue'] = result
	res['rects'] = []
	res['code'] = 0
	return res
	#if result!='':
	#	print 'result = %d'%result


if __name__ == '__main__':
	path = '/data/listtianjin/myimg1476693120655528600.png'
	#binImg = getBinaryImg(path)
	#cv2.imwrite('result.png', binImg)
	#result = getResult(binImg)
	result = recognize_gjj_tianjin(path)
	print result
	#if result!='':
	#	print 'result = %d'%result
