# 外部接口
from flask import Blueprint, request, jsonify
from common.log import logger
from model.result_dto import result_dto
from service import move_service

rancher = Blueprint('rancher', __name__)


# 节点分片调整操作
@rancher.route('/move-peer', methods=['POST'])
def do_adjust():
    try:
        args = request.get_json()
        logger.info(args)
        if not args.get('peerName') or not args.get('neighbors') or not args.get('genesis'):
            return result_dto(False, 401, '参数错误', '')
        # 执行分片移动
        move_service.do_move(args.get('peerName'), args.get('neighbors'), args.get('genesis'))
        return result_dto(True, 200, 'success', '')
    except Exception as e:
        logger.error(e)
        return result_dto(False, 501, 'server failed', str(e))


@rancher.errorhandler(Exception)
def error_500(error):
    logger.error(error)
    return jsonify(result_dto(False, 500, 'server failed', '')), 500