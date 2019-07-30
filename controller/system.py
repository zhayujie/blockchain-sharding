# 内部接口
from flask import Blueprint, request, jsonify
from common.log import logger
from util import json_util
from model.result_dto import result_dto
from service import system_service

system = Blueprint('system', __name__)


# 节点分片调整操作
@system.route('/doAdjust', methods=['POST'])
def do_adjust():
    try:
        args = request.get_json()
        logger.info(args)
        if not args.get('peer_id') or not args.get('chain_id'):
            return result_dto(False, 401, '参数错误', '')
        # 执行分片移动
        system_service.do_move(args.get('peer_id'), args.get('chain_id'))
        return result_dto(True, 200, 'success', '')
    except Exception as e:
        logger.error(e)
        return result_dto(False, 501, 'server failed', str(e))


# 向目标分片节点请求genesis.json文件
@system.route('/getGenesis', methods=['GET'])
def get_genesis():
    target_id = request.args.get('target_id')
    if not target_id:
        return result_dto(False, 401, 'args missing', '')
    # logger.info('target_id: ' + target_id)
    return result_dto(True, 200, 'genesis', system_service.read_genesis(target_id))


@system.errorhandler(Exception)
def error_500(error):
    logger.error(error)
    return jsonify(result_dto(False, 500, 'server failed', '')), 500
