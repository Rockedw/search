#!/bin/bash


d=`date +%s`
python bin/harry_info_server.py >log/err.$d 2>&1 &

