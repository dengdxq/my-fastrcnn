#!/bin/sh
root_path='/home/jiayuan/Documents/checkcode'
img_list=$root_path'/imglist.txt'
train_list=$root_path'/data/ImageSets/train.txt'
imgdir=$root_path'/data/Images'
outxml=$root_path'/data/Annotations'
outmat=$root_path
allbox_path=$root_path'/data/ssbox'
img_type='jpg'


if [ ! -f "$img_list" ];then
    echo "[ERROR]: imglist.txt no exist."
    exit
fi
if [ ! -d "$outxml" ];then
    mkdir -p $outxml
fi
if [ ! -d "$allbox_path" ];then
    mkdir -p $allbox_path
fi

echo "[INFO]: create annotations xml files and trian.txt."
python create_xml.py $img_list $outxml $train_list
echo "[INFO]: finish."

echo "[INFO]: create trian.mat."
python create_train_mat.py $train_list $imgdir $img_type $outmat
echo "[INFO]: finish!"

echo "[INFO]: create all ssboxes.mat."
python create_ssboxes.py $img_list $imgdir $allbox_path
echo "[INFO]: finish!"


