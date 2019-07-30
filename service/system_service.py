from common import config
from common.log import logger
from util import shell_util, request_util, json_util, file_util, yaml_util, string_util
import os
import time

# priv_validator_state.json 文件路径
VALIDATOR_STATE_PATH = os.path.join(os.getcwd(), 'config/priv_validator_state.json')
GENESIS_PATH = 'config/genesis.json'
NEW_POWER = '100'


# 执行节点分片调整
# 1. 删除docker容器
# 2. 数据文件清理，配置文件更新
# 3. 启动容器
# 4. 发送更新验证人请求
# 5. 查询输出日志
def do_move(peer_id, chain_id):
    # 需要转移的节点
    peer = config.get_peer_by_id(peer_id)
    # 目标分片上的锚节点
    target_peer = config.get_peer_by_chain_id(chain_id)

    # 停止容器
    _stop_docker(peer)
    logger.info('容器停止: ' + peer.container_name)

    # 更新配置文件
    _update_files(peer, target_peer)
    logger.info('配置文件更新成功')

    # 启动容器
    _start_docker(peer)
    logger.info('容器启动: ' + peer.container_name)

    # 可能需要sleep
    time.sleep(3)

    # 更新验证人
    _update_validators(peer, target_peer)
    logger.info('验证人更新成功')


# 清除数据文件及更新配置文件
def _update_files(peer, target_peer):
    data_dir = file_util.join(peer.path, 'data')
    # 删除data目录
    file_util.remove(data_dir)

    # 创建data目录并放入 配置文件
    file_util.make_dir(data_dir)
    file_util.copy(VALIDATOR_STATE_PATH, data_dir)

    # 创建docker文件
    _make_docker_file(peer, target_peer)

    # 更新genesis.json文件
    _get_genesis(peer.path, target_peer.ip, target_peer.peer_id)


# 创建docker-compose文件
def _make_docker_file(peer, target_peer):
    # docker文件保存路径
    save_path = file_util.join(peer.path, config.DOCKER_FILE_NAME)

    # 目标分片的锚节点的端口
    target_port = str(int(target_peer.port) - 1)

    # 生产docker-compose文件
    yaml_util.create_docker_file(save_path, peer.container_name, peer.port, peer.path, target_peer.peer_id,
                                 target_peer.ip, target_port)


# 从目标分片获取genesis.json文件并替换
def _get_genesis(path, target_ip, target_id):
    url = str.format('http://{}:{}/api/system/getGenesis', target_ip, config.PORT)
    params = {'target_id': target_id}
    # logger.info(url)
    # 从远程服务获取genesis.json配置
    res = request_util.get(url=url, params=params)
    # logger.info('genesis data: ' + res)
    data = json_util.un_marshal(res)
    if data and data['flag']:
        # 写入文件中
        path = file_util.join(path, GENESIS_PATH)
        file_util.write_json(data['data'], path)
    else:
        raise Exception('获取genesis配置信息失败')


# 发送更新验证人节点的交易
def _update_validators(peer, target_peer):
    pub_key_hex = string_util.base64ToHex(peer.pub_key)
    url = str.format('http://{}:{}/broadcast_tx_commit?tx="val:{}/{}"', target_peer.ip, target_peer.port,
                     pub_key_hex, NEW_POWER)
    res = request_util.get(url)
    logger.info('更新验证人结果: ' + res)


# 停止容器
def _stop_docker(peer):
    if not shell_util.exec_cmd(str.format("docker rm -f {}", peer.container_name)):
        raise Exception('容器删除失败')


# 启动容器
def _start_docker(peer):
    docker_file_path = file_util.join(peer.path, config.DOCKER_FILE_NAME)
    if not shell_util.exec_cmd(str.format("docker-compose -f {} up -d", docker_file_path)):
        raise Exception('容器删除失败')


# 从目标节点读取genesis.json文件
def read_genesis(target_id):
    peer = config.get_peer_by_id(target_id)
    path = file_util.join(peer.path, GENESIS_PATH)
    return file_util.get_json(path)


if __name__ == '__main__':
    config.load_config("../network_config.json")
    do_move("234", "abc")
    print(read_genesis('/Users/zyj/Desktop/node1/node1_data/config/genesis.json'))
