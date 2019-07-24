# 节点结构
class Peer(object):
    def __init__(self, peer_id, chain_id, pub_key, ip, port):
        self.peer_id = peer_id
        self.chain_id = chain_id
        self.pub_key = pub_key
        self.ip = ip
        self.port = port
