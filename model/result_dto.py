# 返回给前端的数据结构
class ResultDTO(object):
    def __init__(self, flag, code, message, data):
        self.flag = flag
        self.code = code
        self.message = message
        self.data = data
