# 返回给前端的数据结构
def result_dto(flag, code, message, data):
    return {
        'flag': flag,
        'code': code,
        'message': message,
        'data': data
    }
