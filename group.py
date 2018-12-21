# -*- coding:utf-8 -*-
# Sharding v0.1

import db
import random
TEST_TX_NUM = 10000
GROUP_NUM = 100
IN_SAME_GROUP= 0
NUM_ADDRS = 0
NUM_NEW_ADDRS = 0
TX_NUM = 0
total_addrs = set({})               # 统计测试交易集中有效地址数量


class Transaction:
    def __init__(self):
        self.in_same_group = 0
        self.addr_num = 0;
        self.groupId = -1;


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


def process_tx(tx):
    # 处理交易   []tx<int>
    groups = []             # 每个地址对应的组              [26, 38, 26, 26, 99...]
    res = {}                # 该交易中每个组号出现的次数     {26:3, 38:1, 99:1}

    global NUM_ADDRS
    NUM_ADDRS += len(tx)

    global TX_NUM
    TX_NUM += 1

    new_address = []

    for address in tx:
        total_addrs.add(address)            # 统计不重复的地址个数

        group_id = db.get_group_id(address)
        if group_id == -1:
            new_address.append(address)     # 新地址单独存放
        else:
            groups.append(group_id)

    # 所有地址都是新地址, 随机选择组号全部加入
    if len(groups) == 0:
        add_new_addrs(new_address, get_random(GROUP_NUM))
        global IN_SAME_GROUP
        IN_SAME_GROUP += 1          # 非跨组交易
        return

    #print('groups', groups)

    # 统计每个组中的账户数量
    for i in groups:
        if not res.get(i):
            res[i] = 1
        else:
            res[i] = res[i] + 1
    #print('res', res)

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

    #print('group_list:', groups_list)
    #print(group_no)

    # 判断 是否该交易 所有地址都在一个组中
    #if len(res) == 1 or (len(res) == 2 and res.get(-1) != None):
    if len(res) == 1:
        global IN_SAME_GROUP
        IN_SAME_GROUP += 1

    # 将新地址加入组中 （组号为该交易大多数地址所在的组）
    if len(new_address) > 0:
        add_new_addrs(new_address, group_no)


# 获取用于测试的交易，该版本会查询所有交易读入内存
# TODO: 需要改进，查询太慢
def input_test_txs(tx_limit, tx_offset=0):
    test_txs = db.get_new_txs(10000, 0)
    print('Finish get all test txs')
    tx = set({})
    start_tx_id = test_txs[0][0]
    for t in test_txs:
        if t[0] == start_tx_id:
            tx.add(t[1])           # 集合中加入输入地址
            tx.add(t[2])           # 集合中加入输出地址
        else:
            #print(tx)
            process_tx(list(tx))
            tx.clear()
            start_tx_id = t[0]
            tx.add(t[1])
            tx.add(t[2])
    process_tx(list(tx))                 # 处理最后一条交易

    print('The first test tx_id: ', test_txs[0][0])
    print('The last test tx_id: ', list(tx)[0])
    #print(tx)


def init_db():
    print('Init the db')
    pass


def print_res():
    print('Tx num: {}'.format(TX_NUM))
    print('Tx num in same group: {}'.format(IN_SAME_GROUP))
    print('Address num: {}'.format(NUM_ADDRS))
    print('Unique address num: {}'.format(len(total_addrs)))
    print('New address num: {}'.format(NUM_NEW_ADDRS))
    #print(db.groups)


if __name__ == '__main__':
    init_db()
    input_test_txs(10000, 0)
    print_res()