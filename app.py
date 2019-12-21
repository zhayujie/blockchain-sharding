from flask import Flask
from controller.tendermint import tendermint
from controller.system import system
from controller.rancher import rancher
from common import config


# 创建flask用用实例
def create_app():
    app = Flask(__name__)
    # 注册蓝本
    app.register_blueprint(tendermint, url_prefix='/api/tendermint')
    app.register_blueprint(system, url_prefix='/api/system')
    app.register_blueprint(rancher, url_prefix='/api/v2/tendermint')
    return app


if __name__ == '__main__':
    # 启动服务
    service = create_app()
    service.run(host=config.HOST, port=config.PORT, threaded=True, debug=True)
