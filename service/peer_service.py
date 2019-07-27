from common import config
from common.log import logger
from util import string_util, request_util, json_util


# 向节点所在机器上的服务 转发分片调整的请求
def transfer_move_req(peer_id, chain_id):
    ip = config.get_peer_ip(peer_id)
    if string_util.is_empty(ip):
        raise Exception("该节点不存在")
    # 向该节点所在机器上的服务发送调整分片的请求
    data = {'peer_id': peer_id, 'chain_id': chain_id}
    url = str.format('http://{}:{}/api/system/doAdjust', ip, config.PORT)
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


# 执行节点分片调整
# 1. 删除docker容器
# 2. 数据文件清理，配置文件更新
# 3. 启动容器
# 4. 发送更新验证人请求
# 5. 查询输出日志
def do_move(peer_id, chain_id):
    pass


# 停止容器
def _stop_docker():
    pass


# 启动容器
def _start_docker():
    pass


# 清除数据文件及更新配置文件
def _update_files():
    pass


# 获取genesis.json文件
def _get_genesis():
    pass


# 更新验证人
def _update_validators():
    pass


if __name__ == '__main__':
    pass
