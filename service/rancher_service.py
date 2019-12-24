from util import json_util, file_util, request_util
from common.config import conf
from common.log import logger
from common import config
import os


# 删除指定服务名称的service
def delete_service(service_name):
    url = str.format('http://{}/v2-beta/projects/{}/services', conf().RANCHER_ADDRESS, conf().PROJECT_ID)
    service_id = _get_service_id(service_name)
    url = str.format(url + '/{}', service_id)
    res = request_util.delete(url)
    logger.info("节点删除中: " + res)


# 启动服务
def create_service(service_name, neighbors):
    url = str.format('http://{}/v2-beta/projects/{}/services', conf().RANCHER_ADDRESS, conf().PROJECT_ID)
    # 读取配置文件
    args_str = file_util.read(conf().RANCHER_TEMPLATE_PATH)

    # 设置参数
    args = _set_docker_config(args_str, service_name, neighbors)

    logger.info(url)

    res = request_util.post(url, args)
    logger.info('节点创建成功: ' + res)


# 根据应用名称获取应用id
def _get_service_id(service_name):
    url = str.format('http://{}/v2-beta/projects/{}/services', conf().RANCHER_ADDRESS, conf().PROJECT_ID)
    res = json_util.un_marshal(request_util.get(url))
    services = res.get('data')
    for service in services:
        if service.get('name') == service_name:
            return service.get('id')


# 根据服务名称获取服务id
def _get_stack_id(stack_name):
    url = str.format('http://{}/v2-beta/projects/{}/stacks', conf().RANCHER_ADDRESS, conf().PROJECT_ID)
    res = json_util.un_marshal(request_util.get(url))
    services = res.get('data')
    for service in services:
        if service.get('name') == stack_name:
            return service.get('id')


# 更新docker配置
def _set_docker_config(args_str, service_name, neighbors):
    args = json_util.un_marshal(args_str)
    peer_dir = os.path.join(conf().NODE_DIR, service_name)
    args['stackId'] = _get_stack_id(conf().STACK_NAME)
    args['name'] = service_name
    args['launchConfig']['hostname'] = service_name
    args['launchConfig']['dataVolumes'] = [str.format('{}:/tendermint', peer_dir)]
    p2p_str = ''
    if neighbors:
        p2p_str = '--p2p.persistent_peers=' + neighbors
    entry_point = ['sh', '-c', str.format('tendermint node {} --proxy_app=persistent_kvstore', p2p_str)]
    args['launchConfig']['entryPoint'] = entry_point
    print(args)
    return args


if __name__ == '__main__':
    config.load_config('dev')
    create_service('TTANode1', '')
    # time.sleep(15)
    # delete_service('TTANode1')
    # logger.info('hello')
    # logger.info(_get_stack_id('test'))
    pass
