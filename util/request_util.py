import requests


# 发送get请求
def get(url, params):
    res = requests.get(url=url, params=params)
    return res.text


# 发送post请求
def post(url, data):
    header = {"content-type": "application/json"}
    res = requests.post(url=url, data=data)
    return res.text
