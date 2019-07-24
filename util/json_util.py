import json


# json对象序列化
def marshal(obj):
    return json.dumps(obj)


# json字符串反序列化
def un_marshal(st):
    return json.loads(st)


if __name__ == '__main__':
    print(marshal({'a': 1}))
    print(un_marshal('{"a": 1}'))
