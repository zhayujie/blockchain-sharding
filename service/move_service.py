from common import config
from common.log import logger
from util import shell_util, request_util, json_util, file_util, yaml_util, string_util
import os
import time


# 执行节点分片调整
# 1. 删除对应rancher服务
# 2. 当前机器数据文件清理，配置文件更新，分发到所有机器上
# 3. 发送请求创建新的rancher服务
def do_move(peer_name, neighbors, genesis):
    pass
