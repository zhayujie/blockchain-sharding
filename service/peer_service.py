from common import config
from common.log import logger
from util import shell_util, request_util, json_util, file_util, yaml_util

VALIDATOR_STATE_PATH = '../config/priv_validator_state.json'


# 向节点所在机器上的服务 转发分片调整的请求
def transfer_move_req(peer_id, chain_id):
    peer = config.get_peer_by_id(peer_id)
    if not peer:
        raise Exception("该节点不存在")
    # 向该节点所在机器上的服务发送调整分片的请求
    data = {'peer_id': peer_id, 'chain_id': chain_id}
    url = str.format('http://{}:{}/api/system/doAdjust', peer.ip, config.PORT)
    try:
        # 转发请求
        res_str = request_util.post(url=url, data=data)
        res = json_util.un_marshal(res_str)
        if res.flag:
            logger.info("调整操作执行成功")
        else:
            raise Exception("调整操作执行失败: " + res.message)
    except Exception as e:
        raise e


# 查询当前网络节点信息(从配置中查)
def get_all_peers():
    pass


# 查询当前网络验证人节点信息
def get_validators():
    pass


if __name__ == '__main__':
    config.load_config("../network_config.json")
