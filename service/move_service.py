from common import config
from common.config import conf
from common.log import logger
from util import shell_util, json_util, file_util
from service import rancher_service
import os


# 创建节点
# 1. 从原节点的拷贝 生成 新节点的目录，加入genesis.json文件，并分发到各机器
# 2. 启动rancher服务
def do_create(old_name, new_name, genesis, neighbors):
    # 分发genesis配置文件
    _update_genesis(old_name, new_name, genesis)

    # 启动rancher服务
    rancher_service.create_service(new_name, neighbors)


# 删除节点
# 1. 删除对应rancher服务
# 2. 备份后 删除所有节点的目录
def do_delete(service_name):
    # 删除rancher服务
    rancher_service.delete_service(service_name)
    # 节点目录为 数据根目录 加上 节点名称
    peer_dir = os.path.join(conf().NODE_DIR, service_name)
    data_dir = os.path.join(peer_dir, 'data')

    # 删除data文件
    file_util.remove(data_dir)

    # 创建data目录并放入 配置文件
    file_util.make_dir(data_dir)
    file_util.copy(conf().VALIDATOR_STATE_PATH, data_dir)

    # bak后缀为副本
    file_util.move_dir(peer_dir, peer_dir + '-bak')

    # 删除其余所有节点的该目录
    for ip in conf().MACHINE_IPS:
        _delete_file(ip, peer_dir)


# 更新genesis配置文件
def _update_genesis(old_name, new_name, genesis):
    # 节点目录为 数据根目录 加上 节点名称,  bak后缀为副本
    old_dir = os.path.join(conf().NODE_DIR, old_name + '-bak')
    new_dir = os.path.join(conf().NODE_DIR, new_name)

    genesis_path = os.path.join(old_dir, 'config/genesis.json')
    # 更新genesis.json文件
    if isinstance(genesis, str):
        genesis = json_util.un_marshal(genesis)
    file_util.write_json(genesis, genesis_path)

    # 移动本地目录到新目录
    file_util.move_dir(old_dir, new_dir)

    # 分发节点目录
    for ip in conf().MACHINE_IPS:
        _distribute_file(ip, new_dir, new_dir)


# 分发机器目录
def _distribute_file(ip, source_dir, target_dir):
    logger.info('开始分发配置文件: ' + ip)
    # 发送文件
    send_cmd = str.format('scp {} -r {} {}@{}:{}', conf().IDENTITY, source_dir, conf().USER_NAME,
                          ip, target_dir)
    send_del = shell_util.exec_cmd(send_cmd)
    logger.info('发送: ' + str(send_del))


# 删除机器目录
def _delete_file(ip, target_dir):
    logger.info('开始删除目录: ' + ip)
    del_str = 'ls'
    if target_dir and '/home/centos/' in target_dir:
        del_str = 'rm -rf ' + target_dir
    # 删除文件
    del_cmd = str.format('ssh {} {}@{} sudo {}', conf().IDENTITY, conf().USER_NAME, ip, del_str)
    res_del = shell_util.exec_cmd(del_cmd)
    logger.info('删除: ' + str(res_del))


if __name__ == '__main__':
    config.load_config('dev')
    name = 'TTANode1'
    p2p_str = 'fd69dfa8baa7cb0dc91a10cdc1eac00506d05b5e@TTANode3:26656'
    genesis_dict = {'genesis_time': '2019-12-21T08:15:49.6296137Z', 'chain_id': 'test-chain-hVOXVd', 'consensus_params': {'block': {'max_bytes': '22020096', 'max_gas': '-1', 'time_iota_ms': '1000'}, 'evidence': {'max_age': '100000'}, 'validator': {'pub_key_types': ['ed25519']}}, 'validators': [{'address': '287CFEDC36CCF61AAA8A6A537BA173F0DF6878E3', 'pub_key': {'type': 'tendermint/PubKeyEd25519', 'value': '+RWAVtjj5uBSPjbp55nulXAcgxQXInxw9lu7CjrbM7U='}, 'power': '1000', 'name': 'tm_node1'}], 'app_hash': ''}
    genesis_str = json_util.marshal(genesis_dict)
    print(genesis_dict)
    # do_move(name, p2p_str, genesis_str)
    peer_source_dir = os.path.join(conf().NODE_DIR, name)
    # _distribute_file('10.77.70.135', peer_source_dir, '/home/centos/zyj/TTANode1')
    do_delete('TTANode3')

    # do_create('TTANode1', 'TTANode2', genesis_dict, p2p_str)
    # 分发免密凭证
    # for count in range(139, 143):
    #     ip = '10.77.70.' + str(count)
    #     _distribute_file(ip, '~/.ssh/id_rsa_768', '/home/centos/.ssh/')


