# -*- coding:utf-8 -*-
# Sharding v0.1

import db
import time
import random
import statistics

# 用于统计的全局实例
stat = statistics.Statistics()


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
        stat.NUM_NEW_ADDRS += 1


def process_tx(txins, txouts):
    # 用于设置标志的的局部实例
    flag = statistics.Flag()
    groups = []             # 每个地址对应的组              [26, 38, 26, 26, 99...]
    new_address = []        # 该交易中新地址的集合
    stat.TX_NUM += 1        # 处理的交易数累加

    # 处理输入集合中的地址
    last_group_id = -1
    for address in txins:
        if is_hub_node(address):
            flag.hub_in = 1
        stat.total_addrs.add(address)                   # 统计不重复的地址个数
        group_id = db.get_group_id(address)             # 查询该地址的组号
        # in中地址不同组
        if group_id != -1 and last_group_id != -1 and group_id != last_group_id:
            flag.diff_in = 1
        if group_id == -1:
            stat.NUM_NEW_IN += 1                # in中的新地址数
            new_address.append(address)         # 新地址单独存放
        else:
            last_group_id = group_id            # 设置上一个地址的组号
            groups.append(group_id)

    # 处理输出集合中的地址
    for address in txouts:
        if is_hub_node(address):
            flag.hub_out = 1
        stat.total_addrs.add(address)            # 统计不重复的地址个数
        group_id = db.get_group_id(address)
        if group_id == -1:
            new_address.append(address)          # 新地址单独存放
        else:
            flag.have_old_out = 1                # out中有旧地址
            groups.append(group_id)

    # 所有地址都是新地址, 随机选择组号全部加入
    if len(groups) == 0:
        add_new_addrs(new_address, get_random(stat.GROUP_NUM))
        stat.IN_SAME_GROUP += 1                  # 非跨组交易
        stat.ALL_NEW_ADDRESS += 1                # 全新交易
        stat.INSIDE_NEW_OUT += 1                 # out全新
        return

    group_no = vote_for_result(groups, flag)     # 投票选出该交易的最终组号
    # 将新地址加入组中 （组号为该交易大多数地址所在的组）
    if len(new_address) > 0:
        add_new_addrs(new_address, group_no)


# 投票选出该交易的组号
def vote_for_result(groups, flag):
    res = {}                        # 该交易中每个组号出现的次数      {26:3, 38:1, 99:1}
    # 统计每个组中的账户数量
    for i in groups:
        if not res.get(i):
            res[i] = 1
        else:
            res[i] = res[i] + 1
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

    # 统计分入的组号
    if not stat.group_ids.get(group_no):
        stat.group_ids[group_no] = 1
    else:
        stat.group_ids[group_no] += 1

    # 给该交易进行分类
    classify_txs(res, flag)
    return group_no


# 对交易进行归类
def classify_txs(res, flag):
    # 组内交易
    if len(res) == 1:
        stat.IN_SAME_GROUP += 1
        if flag.have_old_out == 0:
            stat.INSIDE_NEW_OUT += 1         # 组内：out全为新地址

            if flag.hub_in == 1:
                stat.HUB_IN_0 += 1
            elif flag.hub_out == 1:
                stat.HUB_OUT_0 += 1
            elif flag.hub_in == 0 and flag.hub_out == 0:
                stat.HUB_NO_0 += 1

        else:
            stat.INSIDE_OLD_OUT += 1         # 组内：out中有旧地址，但和in同组

            if flag.hub_in == 1:
                stat.HUB_IN_1 += 1
            elif flag.hub_out == 1:
                stat.HUB_OUT_1 += 1
            elif flag.hub_in == 0 and flag.hub_out == 0:
                stat.HUB_NO_1 += 1
    # 组间交易
    else:
        if flag.diff_in == 1:
            stat.CROSS_DIFF_IN += 1          # 组间：in中地址同组（out和in不同组）

            if flag.hub_in == 1:
                stat.HUB_IN_2 += 1
            elif flag.hub_out == 1:
                stat.HUB_OUT_2 += 1
            elif flag.hub_in == 0 and flag.hub_out == 0:
                stat.HUB_NO_2 += 1
        else:
            stat.CROSS_SAME_IN += 1          # 组间：in中地址不同组

            if flag.hub_in == 1:
                stat.HUB_IN_3 += 1
            elif flag.hub_out == 1:
                stat.HUB_OUT_3 += 1
            elif flag.hub_in == 0 and flag.hub_out == 0:
                stat.HUB_NO_3 += 1


# 获取用于测试的交易，该版本会查询所有交易读入内存
# 需要改进，查询太慢
def input_test_txs(tx_limit, tx_offset=0):

    # test_txs = db.get_new_txs(tx_limit, tx_offset)       # 指定读取多少条测试交易
    test_txs = db.get_new_txs_fast()

    print('Finish get all test txs')
    txins = set({})
    txouts = set({})
    start_tx_id = test_txs[0][0]
    for t in test_txs:
        if t[0] == start_tx_id:
            txins.add(t[1])           # 输入集合中加入地址
            txouts.add(t[2])          # 输出集合中加入地址
        else:
            process_tx(list(txins), list(txouts))
            txins.clear()
            txouts.clear()
            start_tx_id = t[0]
            txins.add(t[1])
            txouts.add(t[2])

    process_tx(list(txins), list(txouts))                 # 处理最后一条交易

    print('The first test tx_id: {}'.format(test_txs[0][0]))
    print('The last test tx_id:  {}'.format(test_txs[-1][0]))


def init_db():
    print('Init the db')
    pass


# 读取hub节点的地址到内存中
def create_hub_table():
    with open('./hub_id.csv') as fs:
        lines = fs.readlines()
        for line in lines:
            stat.hub_list.append(int(line.split(',')[0]))


# 判断是否是hub节点，是则返回True
def is_hub_node(address):
    return address in stat.hub_list


if __name__ == '__main__':
    start_time = time.time()
    # 读取hub节点地址
    create_hub_table()
    # 输入测试交易集
    input_test_txs(0, 0)
    # 输出统计结果
    stat.print_total_stats()
    end_time = time.time()
    # 计算运行时间
    print("Run time: {} s".format(int(end_time - start_time)))
