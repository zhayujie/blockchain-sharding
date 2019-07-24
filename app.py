from flask import Flask
from controller.tendermint import tendermint
from controller.system import system


# 创建flask用用实例
def create_app():
    app = Flask(__name__)

    # 注册蓝本
    app.register_blueprint(tendermint, url_prefix='/tendermint')
    app.register_blueprint(system, url_prefix='/system')

    # 读取配置文件到全局

    return app


if __name__ == '__main__':
    # 启动服务
    create_app().run(port=5000, debug=True)
