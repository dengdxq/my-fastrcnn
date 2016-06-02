#!/usr/bin
cd /home/jiayuan/Documents/download_code/fast-rcnn
#./tools/train_net.py --gpu 0 --solver models/mytrain2/solver.prototxt --weights data/imagenet_models/CaffeNet.v2.caffemodel

#./tools/train_net.py --gpu 0 --solver models/kaggle/solver.prototxt --weights data/imagenet_models/CaffeNet.v2.caffemodel --imdb kaggle_train
./tools/train_net.py --gpu 0 --solver models/checkcode/solver.prototxt --weights data/imagenet_models/CaffeNet.v2.caffemodel --imdb checkcode_train --iters 200000
