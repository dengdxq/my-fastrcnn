#!/bin/sh
#path=`pwd`
nohup python pyscript/tornado_http.py 8181 checkcode_8181.log > http_8181.log &
nohup python pyscript/tornado_http.py 8182 checkcode_8182.log > http_8182.log &
nohup python pyscript/tornado_http.py 8183 checkcode_8183.log > http_8183.log &
#echo $path
