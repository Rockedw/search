#!/bin/bash

git clone https://github.com/facebookresearch/contriever.git
if [ $? -ne 0 ];then
	exit
fi

mkdir data
hadoop fs -get /user/chenjie/search_baseline/data/* data/
if [ $? -ne 0 ];then
	exit
fi

mkdir embeddings
hadoop fs -get /user/chenjie/search_baseline/embeddings/* embeddings/
if [ $? -ne 0 ];then
	exit
fi

mkdir log

