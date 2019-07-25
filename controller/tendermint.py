# 外部接口
from flask import Blueprint, request
from common.log import logger
from util import json_util
from model.result_dto import result_dto

tendermint = Blueprint('tendermint', __name__)


# 网络分片调整
#       peer_id               <str>          需要进行调整的节点id，节点初始化时获得
#       chain_id              <str>          目标分片的Id，与genesis.json文件中相同
@tendermint.route('/movePeer', methods=['POST'])
def move_peer():
    args = json_util.un_marshal(request.get_data(as_text=True))
    if not args.get('peer_id') or not args.get('chain_id'):
        return result_dto(False, 401, "参数错误", "")
    return result_dto(True, 200, "成功", "")


# 查询所有peer的信息
@tendermint.route('/getAllPeers', methods=['GET'])
def get_all_peers():
    return 'getAllPeers'
