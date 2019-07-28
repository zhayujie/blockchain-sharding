import os
from common.log import logger


def exec_cmd(cmd):
    try:
        logger.info("执行命令: " + cmd)
        res = os.system(cmd)
        return True if (res == 0) else False
    except Exception as e:
        logger.error("执行命令出错: ", e)
        return False


if __name__ == '__main__':
    r = exec_cmd('ls abc')
    print(r)
