from util import file_util, json_util
from common.log import logger
import os
import root


class Config:
    VALIDATOR_STATE_PATH = ''
    RANCHER_TEMPLATE_PATH = ''
    ROOT_PATH = ''
    DOCKER_FILE_NAME = ''
    HOST = ''
    PORT = ''
    RANCHER_ADDRESS = ''
    PROJECT_ID = ''
    STACK_NAME = ''
    MACHINE_IPS = []
    USER_NAME = ''
    IDENTITY = ''
    NODE_DIR = ''
    DEBUG = True

    def __init__(self):
        pass


config = Config()


# 加载配置文件
def load_config(env):
    global config
    config_path = os.path.join(root.get_root(), str.format('config/config-{}.json', env))
    # 读取配置文件
    try:
        if not file_util.is_exist(config_path):
            logger.error('配置文件路径不存在')
            return
        config_str = file_util.read(config_path)
        # 将json字符串反序列化为dict类型
        con = json_util.un_marshal(config_str)
        set_config(con)
    except Exception as e:
        logger.error(e)


def set_config(con):
    config.VALIDATOR_STATE_PATH = os.path.join(root.get_root(), 'config/priv_validator_state.json')
    config.RANCHER_TEMPLATE_PATH = os.path.join(root.get_root(), 'config/rancher-template.json')
    config.ROOT_PATH = con.get('ROOT_PATH')
    config.DOCKER_FILE_NAME = con.get('DOCKER_FILE_NAME')
    config.HOST = con.get('HOST')
    config.PORT = con.get('PORT')
    config.RANCHER_ADDRESS = con.get('RANCHER_ADDRESS')
    config.PROJECT_ID = con.get('PROJECT_ID')
    config.STACK_NAME = con.get('STACK_NAME')
    config.MACHINE_IPS = con.get('MACHINE_IPS')
    config.USER_NAME = con.get('USER_NAME')
    config.IDENTITY = con.get('IDENTITY')
    config.NODE_DIR = con.get('NODE_DIR')
    config.DEBUG = con.get('DEBUG')

def conf():
    return config


if __name__ == '__main__':
    load_config('prod')

