#-*- coding:utf-8 –*-
import random
import os
import cv2


def img_binary(imgdata):
	#retval, newimg = cv2.threshold(imgdata, 200, 255, cv2.THRESH_BINARY)
	gimg = imgdata
	if imgdata.shape[2] == 3:
		gimg = cv2.cvtColor(imgdata,cv2.COLOR_BGR2GRAY) 
	#newimg = cv2.adaptiveThreshold(gimg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 5)
	retval, newimg = cv2.threshold(gimg, 100, 255, cv2.THRESH_BINARY)
	#print retval
	return newimg


def splite_rgb_channel(imgdata):	
	if imgdata is None:
		return None
	dim = imgdata.shape
	if dim[2] == 1:
		return imgdata
	imgdict = {}
	imgdict['red'] = imgdata[:,:,2]
	imgdict['green'] = imgdata[:,:,1]
	imgdict['blue'] = imgdata[:,:,0]
	return imgdict


def erase_psbc_image(srcpath):
	img = cv2.imread(srcpath)
	if img is None:
		return None
	rgbimg = img.copy()
	img = splite_rgb_channel(img)
	#print type(img['red'])
	th = 40
	dim = img['red'].shape
	#nimg = img['red'].copy()
	#print dim
	#print dim[0]
	for r in xrange(0,dim[0]):
		for c in xrange(0,dim[1]):
			if img['red'][r,c] < th:
				#nimg[r][c] = 255
				rgbimg[r][c][0] = 233
				rgbimg[r][c][1] = 211
				rgbimg[r][c][2] = 216
	#cv2.imwrite('/home/jiayuan/Desktop/nimg.jpg', rgbimg)
	'''
	for row in img['red']:
		for col in row:
			if col < th:
				print col
	'''
	#return rgbimg
	cv2.imwrite(srcpath, rgbimg)

if __name__ == '__main__':
	path = '/home/jiayuan/Desktop/nimg.jpg'
	'''
	img = cv2.imread(path)
	img = splite_rgb_channel(img)
	#print img
	cv2.imwrite('/home/jiayuan/Desktop/r.jpg', img['red'])
	gimg = img_binary(img['red'])
	cv2.imwrite('/home/jiayuan/Desktop/gray.jpg', gimg)
	'''
	erase_psbc_image(path)