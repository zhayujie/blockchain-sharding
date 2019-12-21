from util import json_util, file_util, request_util
from common import config
from common.log import logger
import time

URL = str.format('http://{}/v2-beta/projects/{}/services', config.RANCHER_ADDRESS, config.PROJECT_ID)


# 删除指定服务名称的service
def delete_service(peer_name):
    service_id = _get_service_id(peer_name)
    url = str.format(URL + '/{}', service_id)
    res = request_util.delete(url)
    logger.info("节点删除中: " + res)


# 启动服务
def create_service(peer_name, neighbors):
    # 读取配置文件
    args_str = file_util.read(config.RANCHER_TEMPLATE_PATH)

    # 设置参数
    args = json_util.un_marshal(args_str)
    args['stackId'] = config.STACK_ID
    args['name'] = peer_name
    args['launchConfig']['hostname'] = peer_name
    print(args)

    logger.info(URL)

    res = request_util.post(URL, args)
    logger.info('节点创建成功: ' + res)


# 根据服务名称获取服务id
def _get_service_id(service_name):
    res = json_util.un_marshal(request_util.get(URL))
    services = res.get('data')
    for service in services:
        if service.get('name') == service_name:
            return service.get('id')


if __name__ == '__main__':
    create_service('TTANode2', '123')
    time.sleep(15)
    delete_service('TTANode2')
    # logger.info('hello')
