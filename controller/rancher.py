# 外部接口
from flask import Blueprint, request, jsonify
from common.log import logger
from model.result_dto import result_dto
from service import move_service

rancher = Blueprint('rancher', __name__)


# 节点创建操作
@rancher.route('/create-peer', methods=['POST'])
def do_create():
    try:
        args = request.get_json()
        logger.info(args)
        if not args.get('peerName') or not args.get('newPeerName') or not args.get('genesis') or not args.get('neighbors'):
            return result_dto(False, 401, '参数错误', '')
        # 创建节点
        move_service.do_create(args.get('peerName'), args.get('newPeerName'), args.get('genesis'), args.get('neighbors'))
        return result_dto(True, 200, '创建节点成功', '')
    except Exception as e:
        logger.error(e)
        return result_dto(False, 501, 'server failed', str(e))


# 节点删除操作
@rancher.route('/delete-peer', methods=['GET'])
def do_delete():
    try:
        args = request.args
        logger.info(args)
        if not args.get('peerName'):
            return result_dto(False, 401, '参数错误', '')
        # 删除节点
        move_service.do_delete(args.get('peerName'))
        return result_dto(True, 200, '删除成功', '')
    except Exception as e:
        logger.error(e)
        return result_dto(False, 501, 'server failed', str(e))


@rancher.errorhandler(Exception)
def error_500(error):
    logger.error(error)
    return jsonify(result_dto(False, 500, 'server failed', str(error))), 500
