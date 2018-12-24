# -*- coding:utf-8 -*-
# Sharding v0.1


class Statistics:
    def __init__(self):
        self.GROUP_NUM = 100             # 组数
        self.IN_SAME_GROUP = 0           # 组内交易个数
        self.NUM_NEW_ADDRS = 0           # 新地址的个数
        self.TX_NUM = 0                  # 输入的测试交易个数

        self.total_addrs = set({})       # 统计测试交易集中有效地址数量
        self.hub_list = []               # 保存hub节点地址的list
        self.group_ids = {}              # 测试集被分入的各组号数量统计

        self.ALL_NEW_ADDRESS = 0         # 所有地址都是新地址的交易数
        self.NUM_NEW_IN = 0              # in中出现的新地址数

        self.INSIDE_NEW_OUT = 0          # 组内：out全新
        self.INSIDE_OLD_OUT = 0          # 组内：out有旧的，但和in同组
        self.CROSS_DIFF_IN = 0           # 组间：in不同组
        self.CROSS_SAME_IN = 0           # 组间：in同组，out和in不同组

        self.HUB_IN_0 = 0
        self.HUB_OUT_0 = 0
        self.HUB_NO_0 = 0
        self.HUB_IN_1 = 0
        self.HUB_OUT_1 = 0
        self.HUB_NO_1 = 0
        self.HUB_IN_2 = 0
        self.HUB_OUT_2 = 0
        self.HUB_NO_2 = 0
        self.HUB_IN_3 = 0
        self.HUB_OUT_3 = 0
        self.HUB_NO_3 = 0

    def print_total_stats(self):
        print('输入交易数: {}'.format(self.TX_NUM))
        print('组内交易数: {}'.format(self.IN_SAME_GROUP))
        print('非重复地址数: {}'.format(len(self.total_addrs)))
        print('新增地址数: {}'.format(self.NUM_NEW_ADDRS))

        print('所有地址都是新地址的交易数: {}'.format(self.ALL_NEW_ADDRESS))
        print('in中出现的新地址数: {}'.format(self.NUM_NEW_IN))
        print('')

        print('组内：out全新: {}, hub_in: {}, hub_out: {}, hub_no: {}'.format(self.INSIDE_NEW_OUT,
            self.HUB_IN_0, self.HUB_OUT_0, self.HUB_NO_0))
        print('组内：out有旧的，但和in同组: {}, hub_in: {}, hub_out: {}, hub_no: {}'.format(self.INSIDE_OLD_OUT,
            self.HUB_IN_1, self.HUB_OUT_1, self.HUB_NO_1))

        print('')
        print('组间：in不同组: {}, hub_in: {}, hub_out: {}, hub_no: {}'.format(self.CROSS_DIFF_IN,
            self.HUB_IN_2, self.HUB_OUT_2, self.HUB_NO_2))
        print('组间：in同组，out和in不同组: {}, hub_in: {}, hub_out: {}, hub_no: {}'.format(self.CROSS_SAME_IN,
            self.HUB_IN_3, self.HUB_OUT_3, self.HUB_NO_3))

        print(self.group_ids)


class Flag:
    def __init__(self):
        self.have_old_out = 0           # 0: out全是新地址     1: out中有旧地址
        self.diff_in = 0                # 0: in中地址同组      1: in中地址不同组
        self.hub_in = 0                 # 0: hub未出现在in中   1: hub出现在in中
        self.hub_out = 0                # 0: hub未出现在out中  1: hub出现在out中
