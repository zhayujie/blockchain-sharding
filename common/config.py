from util import file_util, json_util
from model.peer import Peer
from common.log import logger
import os
import root

# 私有全局变量，网络中所有节点的信息
__network_peers = []

# 项目根目录
ROOT_PATH = root.get_root()

# 配置文件路径
CONFIG_PATH = './network_config.json'

# 服务监听ip
HOST = '0.0.0.0'

# 服务监听端口
PORT = 5000

# docker配置文件名称
DOCKER_FILE_NAME = 'docker-compose.yaml'

# priv_validator_state.json 文件路径
VALIDATOR_STATE_PATH = os.path.join(ROOT_PATH, 'config/priv_validator_state.json')

# rancher模版文件路径
RANCHER_TEMPLATE_PATH = os.path.join(ROOT_PATH, 'config/rancher-template.json')

# rancher 服务器地址
# RANCHER_ADDRESS = "10.77.135.8888"
RANCHER_ADDRESS = "127.0.0.1:8080"

# env ID
PROJECT_ID = "1a5"

# stack ID
STACK_ID = "1st10"





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
    print(RANCHER_TEMPLATE_PATH)


