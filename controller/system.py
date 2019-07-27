# 内部接口
from flask import Blueprint, request, jsonify
from common.log import logger
from util import json_util
from model.result_dto import result_dto

system = Blueprint('system', __name__)


# 节点分片调整操作
@system.route('/doAdjust', methods=['POST'])
def do_adjust():
    args = request.get_json()
    logger.info(args)
    return result_dto(True, 200, 'success', '')


# 向目标分片节点请求genesis.json文件
@system.route('/getGenesis', methods=['GET'])
def get_genesis():
    return 'getGenesis'


@system.errorhandler(Exception)
def error_500(error):
    logger.error(error)
    return jsonify(result_dto(False, 500, 'server failed', '')), 500
