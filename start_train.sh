#!/usr/bin
cd /data/code/my-fastrcnn
#./tools/train_net.py --gpu 0 --solver models/mytrain2/solver.prototxt --weights data/imagenet_models/CaffeNet.v2.caffemodel

#./tools/train_net.py --gpu 0 --solver models/kaggle/solver.prototxt --weights data/imagenet_models/CaffeNet.v2.caffemodel --imdb kaggle_train
./tools/train_net.py --gpu 0 --solver models/checkcode_vgg16/solver.prototxt --weights data/imagenet_models/VGG16.v2.caffemodel --imdb checkcode_train --iters 600000
