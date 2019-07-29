from common import config
from common.log import logger
from util import shell_util, request_util, json_util, file_util, yaml_util

VALIDATOR_STATE_PATH = '../config/priv_validator_state.json'


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
    # _stop_docker(peer.container_name)

    # 更新配置文件
    _update_files(peer, target_peer)

    # 启动容器
    docker_file_path = file_util.join(peer.path, config.DOCKER_FILE_NAME)
    _start_docker(docker_file_path)

    # 更新验证人 TODO


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

    # 更新genesis.json文件 TODO
    _get_genesis(target_peer.ip, target_peer.path)


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
def _get_genesis(target_ip, target_path):
    pass


# 更新验证人节点
def _update_validators():
    pass


# 停止容器
def _stop_docker(container_name):
    if not shell_util.exec_cmd(str.format("docker rm -f {}", container_name)):
        raise Exception('容器删除失败')


# 启动容器
def _start_docker(docker_file_path):
    if not shell_util.exec_cmd(str.format("docker-compose -f {} up -d", docker_file_path)):
        raise Exception('容器删除失败')


# 获取genesis.json文件
def read_genesis(path):
    return file_util.get_json(path)


if __name__ == '__main__':
    config.load_config("../network_config.json")
    do_move("234", "abc")
    print(read_genesis('/Users/zyj/Desktop/node1/node1_data/config/genesis.json'))
