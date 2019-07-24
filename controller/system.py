# 内部接口
from flask import Blueprint

system = Blueprint('system', __name__)


# 节点分片调整操作
@system.route('/doAdjust', methods=['GET'])
def do_adjust():
    return 'doAdjust'


# 向目标分片节点请求genesis.json文件
@system.route('/getGenesis', methods=['GET'])
def get_genesis():
    return 'getGenesis'
