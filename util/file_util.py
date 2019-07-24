import os


# 读取文件所有内容
def read(path):
    f = open(path, 'r')
    return f.read()


# 写入文件
def write():
    pass


if __name__ == '__main__':
    print(os.getcwd())
    file_path = "../network_config.json"
    print(read(file_path))

