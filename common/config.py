from util import file_util, json_util
from model.peer import Peer
from common.log import logger

# 私有全局变量，网络中所有节点的信息
__network_peers = []

# 配置文件路径
CONFIG_PATH = './network_config.json'

# 服务监听端口
PORT = 5000

# docker配置文件名称
DOCKER_FILE_NAME = 'docker-compose.yaml'


# 加载配置文件
def load_config(config_path=CONFIG_PATH):
    # 读取配置文件
    try:
        if not file_util.is_exist(config_path):
            logger.error('配置文件路径不存在')
            return
        config_str = file_util.read(config_path)
        # 将json字符串反序列化为dict类型
        peers_config = json_util.un_marshal(config_str)
        for peer_config in peers_config['peers']:
            # 将dict转化为Peer对象, 并在list中追加
            __network_peers.append(Peer.dict2peer(peer_config))
    except Exception as e:
        logger.error(e)


# 获取网络节点信息
def get_config():
    return __network_peers


# 根据节点id查询所在机器ip
def get_peer_by_id(peer_id):
    for peer_info in __network_peers:
        if peer_info.peer_id == peer_id:
            return peer_info
    raise Exception('未找到节点')


# 根据chain_id获取其中某一个节点
def get_peer_by_chain_id(chain_id):
    for peer_info in __network_peers:
        if peer_info.chain_id == chain_id:
            return peer_info
    raise Exception('未找到节点')


if __name__ == '__main__':
    load_config("../network_config.json")
    peer = get_peer_by_id('123')
    print(peer.container_name)
    # load_config()
    # print(get_config()[0].to_string())

