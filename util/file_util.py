import os


# 读取文件所有内容
def read(path):
    with open(path, 'r') as f:
        return f.read()


# 写入文件
def write():
    pass


# 删除文件
def remove(path):
    pass


# 判断文件是否存在
def if_exist(path):
    return os.path.isfile(path)


if __name__ == '__main__':
    file_path = "../network_config.json"
    print(if_exist(file_path))

