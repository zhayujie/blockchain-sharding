import yaml
from common.log import logger
from collections import OrderedDict


# 保证dict写入yaml文件的顺序
def ordered_yaml_dump(data, stream=None, Dumper=yaml.SafeDumper, **kwds):
    class OrderedDumper(Dumper):
        pass
    def _dict_representer(dumper, data):
        return dumper.represent_mapping(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, data.items())
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)


# 生产docker-compose启动文件
def create_docker_file(save_path, container_name, abci_port, path, target_peer_id, target_ip, target_port):
    entry_str = str.format('tendermint node --p2p.seeds={}@{}:{} --proxy_app=persistent_kvstore', target_peer_id,
                           target_ip, target_port)
    node = OrderedDict()
    node['image'] = 'tendermint/tendermint:latest'
    node['container_name'] = container_name
    node['hostname'] = container_name
    node['tty'] = 'true'
    node['ports'] = [abci_port+':26657', str(int(abci_port)-1)+':26656']
    node['volumes'] = [path + ':/tendermint']
    node['environment'] = ['TASKID=C']
    node['entrypoint'] = ['sh', '-c', entry_str]
    docker_config = OrderedDict()
    docker_config['version'] = '2.0'
    docker_config['services'] = {container_name: node}

    with open(save_path, 'w') as f:
        ordered_yaml_dump(docker_config, f, default_flow_style=False)
