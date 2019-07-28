from util import file_util, json_util


# 节点结构
class Peer(object):
    def __init__(self, peer_id, chain_id, pub_key, ip, port, container_name, path):
        self.peer_id = peer_id
        self.chain_id = chain_id
        self.pub_key = pub_key
        self.ip = ip
        self.port = port
        self.container_name = container_name
        self.path = path

    @staticmethod
    def dict2peer(peer_dict):
        return Peer(peer_dict["peer_id"], peer_dict["chain_id"], peer_dict["pub_key"], peer_dict["ip"],
                    peer_dict["port"], peer_dict["container_name"], peer_dict["path"])

    @staticmethod
    def peer2dict(peer):
        return {
            "peer_id": peer.port,
            "chain_id": peer.chain_id,
            "pub_key": peer.pub_key,
            "ip": peer.ip,
            "port": peer.port,
            "container_name": peer.container_name,
            "path": peer.path
        }

    def to_string(self):
        return json_util.marshal(Peer.peer2dict(self))
