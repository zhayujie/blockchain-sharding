# -*- coding:utf-8 -*-
# Sharding v0.1

import db
import time
import random

GROUP_NUM = 100                     # 组数
IN_SAME_GROUP = 0                   # 组内交易个数
#NUM_ADDRS = 0
NUM_NEW_ADDRS = 0                   # 新地址的个数
TX_NUM = 0                          # 输入的测试交易个数
total_addrs = set({})               # 统计测试交易集中有效地址数量

ALL_NEW_ADDRESS = 0                 # 所有地址都是新地址的交易数

NUM_NEW_IN = 0                      # in中出现的新地址数

INSIDE_NEW_OUT = 0                  # 组内：out全新
INSIDE_OLD_OUT = 0                  # 组内：out有旧的，但和in同组
CROSS_DIFF_IN = 0                   # 组间：in不同组
CROSS_SAME_IN = 0                   # 组间：in同组，out和in不同组

HUB_IN_0 = 0
HUB_OUT_0 = 0
HUB_NO_0 = 0
HUB_IN_1 = 0
HUB_OUT_1 = 0
HUB_NO_1 = 0
HUB_IN_2 = 0
HUB_OUT_2 = 0
HUB_NO_2 = 0
HUB_IN_3 = 0
HUB_OUT_3 = 0
HUB_NO_3 = 0

hub_list = []                       # 保存hub节点地址的list


"""
class Address:
    def __init__(self, ):
        self.in_same_group = 0
        self.addr_num = 0;
        self.groupId = -1;
"""


# 生成 0 ~ size-1 的随机数
def get_random(size):
    return random.randint(0, size-1)


# 在一个数列里生成随机数
def get_random_in_list(nums):
    random_index = get_random(len(nums))
    return nums[random_index]


# 新地址 添加入分组
def add_new_addrs(new_addrs, group_id):
    if not new_addrs:
        return
    for i in new_addrs:
        db.insert_new_tx(i, group_id)
        global NUM_NEW_ADDRS
        NUM_NEW_ADDRS += 1


def process_tx(txins, txouts):

    # 全局变量声明
    global IN_SAME_GROUP
    global ALL_NEW_ADDRESS
    global NUM_NEW_IN
    global INSIDE_NEW_OUT
    global INSIDE_OLD_OUT
    global CROSS_DIFF_IN
    global CROSS_SAME_IN

    global HUB_IN_0
    global HUB_OUT_0
    global HUB_NO_0

    global HUB_IN_1
    global HUB_OUT_1
    global HUB_NO_1

    global HUB_IN_2
    global HUB_OUT_2
    global HUB_NO_2

    global HUB_IN_3
    global HUB_OUT_3
    global HUB_NO_3

    # 局部标记变量
    have_old_out = 0            # 0: out全是新地址   1: out中有旧地址
    diff_in = 0                 # 0: in中地址同组    1: in中地址不同组
    hub_in = 0                  # 0: hub未出现在in中   1: hub出现在in中
    hub_out = 0                 # 0: hub未出现在out中  1: hub出现在out中

    # 处理交易   []tx<int>
    groups = []             # 每个地址对应的组              [26, 38, 26, 26, 99...]
    res = {}                # 该交易中每个组号出现的次数     {26:3, 38:1, 99:1}

    # global NUM_ADDRS
    # NUM_ADDRS += len(tx)

    global TX_NUM
    TX_NUM += 1

    new_address = []

    # 处理输入集合中的地址
    last_group_id = -1
    for address in txins:
        if is_hub_node(address):
            hub_in = 1
        total_addrs.add(address)                # 统计不重复的地址个数

        group_id = db.get_group_id(address)

        # in中地址不同组
        if group_id != -1 and last_group_id != -1 and group_id != last_group_id:
            diff_in = 1

        if group_id == -1:
            NUM_NEW_IN += 1                     # in中的新地址数
            new_address.append(address)         # 新地址单独存放
        else:
            groups.append(group_id)
            last_group_id = group_id            # 设置上一个地址的组号


    # 处理输出集合中的地址
    for address in txouts:
        if is_hub_node(address):
            hub_out = 1

        total_addrs.add(address)            # 统计不重复的地址个数

        group_id = db.get_group_id(address)
        if group_id == -1:
            new_address.append(address)     # 新地址单独存放
        else:
            have_old_out = 1                # out中有旧地址
            groups.append(group_id)

    # 所有地址都是新地址, 随机选择组号全部加入
    if len(groups) == 0:
        add_new_addrs(new_address, get_random(GROUP_NUM))
        IN_SAME_GROUP += 1          # 非跨组交易

        ALL_NEW_ADDRESS += 1        # 全新交易
        INSIDE_NEW_OUT += 1         # out全新
        return

    # print('groups', groups)

    # 统计每个组中的账户数量
    for i in groups:
        if not res.get(i):
            res[i] = 1
        else:
            res[i] = res[i] + 1
    # print('res', res)

    # 统计各组中的地址个数
    max = 0
    groups_list = []
    for i in res.keys():            # i: 组号
        if max < res[i]:
            max = res[i]
            groups_list = []
            groups_list.append(i)
        elif max == res[i]:
            groups_list.append(i)
    group_no = 0

    # 得出一个最终的分组
    if len(groups_list) == 1:
        group_no = groups_list[0]
    elif groups_list:
        group_no = get_random_in_list(groups_list)

    # print('group_list:', groups_list)
    # print(group_no)

    # 判断 是否该交易 所有地址都在一个组中
    # if len(res) == 1 or (len(res) == 2 and res.get(-1) != None):

    # 组内交易
    if len(res) == 1:
        IN_SAME_GROUP += 1
        if have_old_out == 0:
            INSIDE_NEW_OUT += 1         # 组内：out全为新地址

            if hub_in == 1:
                HUB_IN_0 += 1
            elif hub_out == 1:
                HUB_OUT_0 += 1
            elif hub_in == 0 and hub_out == 0:
                HUB_NO_0 += 1

        else:
            INSIDE_OLD_OUT += 1         # 组内：out中有旧地址，但和in同组

            if hub_in == 1:
                HUB_IN_1 += 1
            elif hub_out == 1:
                HUB_OUT_1 += 1
            elif hub_in == 0 and hub_out == 0:
                HUB_NO_1 += 1

    # 组间交易
    else:
        if diff_in == 1:
            CROSS_DIFF_IN += 1          # 组间：in中地址同组（out和in不同组）

            if hub_in == 1:
                HUB_IN_2 += 1
            elif hub_out == 1:
                HUB_OUT_2 += 1
            elif hub_in == 0 and hub_out == 0:
                HUB_NO_2 += 1

        else:
            CROSS_SAME_IN += 1          # 组间：in中地址不同组

            if hub_in == 1:
                HUB_IN_3 += 1
            elif hub_out == 1:
                HUB_OUT_3 += 1
            elif hub_in == 0 and hub_out == 0:
                HUB_NO_3 += 1

    # 将新地址加入组中 （组号为该交易大多数地址所在的组）
    if len(new_address) > 0:
        add_new_addrs(new_address, group_no)


# 获取用于测试的交易，该版本会查询所有交易读入内存
# 需要改进，查询太慢
def input_test_txs(tx_limit, tx_offset=0):

    test_txs = db.get_new_txs(tx_limit, tx_offset)       # 指定读取多少条测试交易
    # test_txs = db.get_new_txs_fast()

    print('Finish get all test txs')
    txins = set({})
    txouts = set({})
    start_tx_id = test_txs[0][0]
    for t in test_txs:
        if t[0] == start_tx_id:
            txins.add(t[1])           # 输入集合中加入地址
            txouts.add(t[2])          # 输出集合中加入地址
        else:
            # print(tx)
            process_tx(list(txins), list(txouts))
            txins.clear()
            txouts.clear()
            start_tx_id = t[0]
            txins.add(t[1])
            txouts.add(t[2])

    process_tx(list(txins), list(txouts))                 # 处理最后一条交易

    print('The first test tx_id: {}'.format(test_txs[0][0]))
    print('The last test tx_id:  {}'.format(test_txs[-1][0]))
    # print(tx)


def init_db():
    print('Init the db')
    pass


def create_hub_table():
    with open('./hub_id.csv') as fs:
        lines = fs.readlines()
        for line in lines:
            hub_list.append(int(line.split(',')[0]))


def is_hub_node(address):
    return address in hub_list


def print_res():
    print('输入交易数: {}'.format(TX_NUM))
    print('组内交易数: {}'.format(IN_SAME_GROUP))
    # print('Address num: {}'.format(NUM_ADDRS))
    print('非重复地址数: {}'.format(len(total_addrs)))
    print('新增地址数: {}'.format(NUM_NEW_ADDRS))
    # print(db.groups)

    print('所有地址都是新地址的交易数: {}'.format(ALL_NEW_ADDRESS))
    print('in中出现的新地址数: {}'.format(NUM_NEW_IN))
    print('')

    print('组内：out全新: {}, hub_in: {}, hub_out: {}, hub_no: {}'.format(INSIDE_NEW_OUT,
          HUB_IN_0, HUB_OUT_0, HUB_NO_0))
    print('组内：out有旧的，但和in同组: {}, hub_in: {}, hub_out: {}, hub_no: {}'.format(INSIDE_OLD_OUT,
          HUB_IN_1, HUB_OUT_1, HUB_NO_1))

    print('')
    print('组间：in不同组: {}, hub_in: {}, hub_out: {}, hub_no: {}'.format(CROSS_DIFF_IN,
          HUB_IN_2, HUB_OUT_2, HUB_NO_2))
    print('组间：in同组，out和in不同组: {}, hub_in: {}, hub_out: {}, hub_no: {}'.format(CROSS_SAME_IN,
          HUB_IN_3, HUB_OUT_3, HUB_NO_3))


if __name__ == '__main__':
    a = time.time()
    # init_db()
    create_hub_table()
    input_test_txs(10000, 0)
    print_res()
    b = time.time()
    print("Run time: {}".format(b-a))