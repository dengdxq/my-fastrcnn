#!/bin/sh
imglist='/home/jiayuan/Documents/checkcode/imglist.txt'
trainlist='/home/jiayuan/Documents/checkcode/data/ImageSets/train.txt'
imgdir='/home/jiayuan/Documents/checkcode/data/Images'
outxml='/home/jiayuan/Documents/checkcode/test/Annotations'
outmat='/home/jiayuan/Documents/checkcode/test'


#python create_train_mat.py $trainlist $imgdir jpg $outmat 
#echo "create mat finish!"
python create_xml.py $imglist $outxml  
echo "create xml finish!"
