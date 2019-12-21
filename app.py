from flask import Flask
from controller.tendermint import tendermint
from controller.system import system
from controller.rancher import rancher
from common import config
from common.log import logger
import sys


# 创建flask用用实例
def create_app():
    app = Flask(__name__)
    # 注册蓝本
    app.register_blueprint(tendermint, url_prefix='/api/tendermint')
    app.register_blueprint(system, url_prefix='/api/system')
    app.register_blueprint(rancher, url_prefix='/api/v2/tendermint')
    return app


# 加载环境
def load_env(args):
    env = 'dev'
    if len(args) > 1:
        arg = args[1].split('=')
        if len(arg) > 1 and arg[0] == '--active' and arg[1] == 'prod':
            env = arg[1]
    logger.info('当前环境为: ' + env)
    config.load_config(env)


if __name__ == '__main__':
    # 加载配置
    load_env(sys.argv)
    # 启动服务
    service = create_app()
    service.run(host=config.conf().HOST, port=config.conf().PORT, threaded=True, debug=config.conf().DEBUG)
