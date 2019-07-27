from util import file_util, json_util
from model.peer import Peer
import logging

# 私有全局变量，网络中所有节点的信息
__network_peers = []

# 配置文件路径
CONFIG_PATH = "./network_config.json"

# 服务监听端口
PORT = 5000


# 加载配置文件
def load_config():
    # 读取配置文件
    try:
        if not file_util.if_exist(CONFIG_PATH):
            return
        config_str = file_util.read(CONFIG_PATH)
        # 将json字符串反序列化为dict类型
        peers_config = json_util.un_marshal(config_str)
        for peer_config in peers_config['peers']:
            # 将dict转化为Peer对象, 并在list中追加
            __network_peers.append(Peer.dict2peer(peer_config))
    except Exception as e:
        logging.error(e)


# 获取网络节点信息
def get_config():
    return __network_peers


# 根据节点id查询所在机器ip
def get_peer_ip(peer_id):
    for peer in __network_peers:
        if peer.peer_id == peer_id:
            return peer.ip
    return None


if __name__ == '__main__':
    load_config()
    print(get_config()[0].to_string())

