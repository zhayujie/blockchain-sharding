# 外部接口
from flask import Blueprint

tendermint = Blueprint('tendermint', __name__)


# 网络分片调整
#       peer_id               <str>          需要进行调整的节点id，节点初始化时获得
#       chain_id              <str>          目标分片的Id，与genesis.json文件中相同
@tendermint.route('/movePeer', methods=['GET'])
def move_peer():
    return 'movePeer'


# 查询所有peer的信息
@tendermint.route('/getAllPeers', methods=['GET'])
def get_all_peers():
    return 'getAllPeers'
