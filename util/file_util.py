import os
import shutil


# 读取文件所有内容
def read(path):
    with open(path, 'r') as f:
        return f.read()


# 写入文件
def write():
    pass


# 删除文件或目录
def remove(path):
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)
    else:
        raise Exception('文件或目录不存在')


# 复制文件到指定目录
def copy(src, dst):
    if is_exist(src) and is_exist(dst):
        shutil.copy(src, dst)
    else:
        raise Exception('复制失败: 路径不存在')


# 创建目录
def make_dir(path):
    if not is_exist(path):
        os.mkdir(path)
    else:
        raise Exception('路径已存在')


# 判断文件是否存在
def is_exist(path):
    return os.path.exists(path)


# 路径拼接
def join(d, path):
    return os.path.join(d, path)


if __name__ == '__main__':
    file_path = "../network_config.json"
    print(is_exist(file_path))
    print(join('/ubuntu', 'data'))

