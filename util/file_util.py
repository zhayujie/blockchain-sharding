import os
import shutil
import json


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
        raise Exception('复制失败: 路径不存在, src: ' + src + ' dst: ' + dst)


# 复制整个目录
def copy_dir(src, dst):
    if is_exist(src):
        shutil.copytree(src, dst)
    else:
        raise Exception('复制失败: 路径不存在, src: ' + src + ' dst: ' + dst)


# 移动目录
def move_dir(src, dst):
    if not is_exist(dst):
        shutil.move(src, dst)
    else:
        raise Exception('路径已存在')


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


# 获取json文件内容
def get_json(path):
    if is_exist(path):
        with open(path, 'r', encoding='utf-8') as f:
            # 注意, loads() 是从字符串中读取
            return json.load(f)
    else:
        raise Exception('文件不存在')


# 将json数据写入文件
def write_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        # 注意, dump() 是写入dict
        return json.dump(data, f)


if __name__ == '__main__':
    # file_path = "../network_config.json"
    # print(is_exist(file_path))
    print(join('/ubuntu', 'data'))
    print(os.getcwd())
    copy_dir('/Users/zyj/Desktop/sharding', '/Users/zyj/Desktop/sharding-bak')
