# 外部接口
from flask import Blueprint, request, jsonify
from common.log import logger
from util import json_util
from model.result_dto import result_dto
from service import peer_service

tendermint = Blueprint('tendermint', __name__)


# 网络分片调整
#       peer_id               <str>          需要进行调整的节点id，节点初始化时获得
#       chain_id              <str>          目标分片的Id，与genesis.json文件中相同
@tendermint.route('/movePeer', methods=['POST'])
def move_peer():
    # args = json_util.un_marshal(request.get_data(as_text=True))
    args = request.get_json()
    logger.info(args)
    if not args.get('peer_id') or not args.get('chain_id'):
        return result_dto(False, 401, "参数错误", "")
    # 转发移动分片的请求
    try:
        peer_service.transfer_move_req(args.get('peer_id'), args.get('chain_id'))
        return result_dto(True, 200, "成功", "")
    except Exception as e:
        logger.error("分片调整失败" + str(e))
        return result_dto(False, 500, "失败", str(e))


# 查询所有peer的信息
@tendermint.route('/getAllPeers', methods=['GET'])
def get_all_peers():
    return 'getAllPeers'


@tendermint.errorhandler(Exception)
def error_500(error):
    logger.error(error)
    return jsonify(result_dto(False, 500, 'server failed', '')), 500
