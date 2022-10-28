#!/usr/bin/python

from wsgiref.simple_server import make_server
import json
import urllib.parse
import datetime
import main_conf

import os
import sys

sys.path.append(main_conf.home_path)
sys.path.append(main_conf.home_path+'/contriever')

import esearch

#输出回复时，通过string.encode()指定输出的文字编码方式，string.encode('gb2312')、string.encode('utf-8')、string.encode('gbk')
errStr ='''
{ 
	"code" : -1, 
	"msg" : "not support"
}
'''

esearch_obj = esearch.ESearch('221020_01','harry_data.jsonl','facebook/mcontriever')
esearch_obj_v2 = esearch.ESearch('221025_00','harry_data_v2.jsonl','facebook/mcontriever-msmarco')

def RunServer(environ, start_response):

    #添加回复内容的HTTP头部信息，支持多个
    headers = {'Content-Type': 'application/json', 'Custom-head1': 'Custom-info1'}

    # environ 包含当前环境信息与请求信息，为字符串类型的键值对
    current_url = environ['PATH_INFO']
	
    current_request_method = environ['REQUEST_METHOD']
    current_remote_address = environ['REMOTE_ADDR']
    current_remote_querys = {}
    try:
        for pair in environ['QUERY_STRING'].split('&'):
            k,v = pair.split('=')
            current_remote_querys[k] = v
    except:
            start_response("404 not found", list(headers.items()))
            return [errStr.encode("utf-8"), ]
    '''
    HTTP客户端请求的其他头部信息（Host、Connection、Accept等），对应environ内容为“HTTP_XXX”，
    例如：请求头部为"custom-header: value1",想获取custom-header的值使用如下方式：
    '''
    #current_custom_header = environ['HTTP_CUSTOM_HEADER']

    #print("environ:", environ)
    print('REQUEST time:', datetime.datetime.now())
    print("REQUEST remote ip:", current_remote_address)
    print("REQUEST method:", current_request_method)
    print("REQUEST URL:", current_url)
    print("REQUEST QUERYS:", current_remote_querys)
    #print("REQUEST Custom-header:", current_custom_header)

    #根据不同URL回复不同内容
    if current_url == "/search" and 'query' in current_remote_querys:
        start_response("200 OK", list(headers.items()))
        query = current_remote_querys['query']
        query = urllib.parse.unquote(query)
        if 'v' in current_remote_querys and current_remote_querys['v'] == '2':
            resp = json.dumps(esearch_obj_v2.get_top_n(query), ensure_ascii=False)
        else:
            resp = json.dumps(esearch_obj.get_top_n(query), ensure_ascii=False)
        print(resp)
        return [resp.encode("utf-8"), ]
		#return [json.dumps(esearch_obj.get_top_5('小冰董事长是谁')).encode("utf-8")]

    else:
        start_response("404 not found", list(headers.items()))
        return [errStr.encode("utf-8"), ]

if __name__ == "__main__":
    #10000为HTTP服务监听端口，自行修改
    httpd = make_server('', 59002, RunServer)
    host, port = httpd.socket.getsockname()
    print('Serving running', host, 'port', port)
    httpd.serve_forever()

