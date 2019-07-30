import requests
from util import json_util


# 发送get请求
def get(url, params=None):
    res = requests.get(url=url, params=params)
    return res.text


# 发送post请求
def post(url, data):
    header = {"content-type": "application/json"}
    # post发送json数据需要指定headers，并且对data进行序列化
    res = requests.post(url=url, data=json_util.marshal(data), headers=header)
    return res.text
