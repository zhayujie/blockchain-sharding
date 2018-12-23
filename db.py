# -*- coding:utf-8 -*-
# Sharding v0.1

import psycopg2

#groups = {0:3, 1:3, 2:5, 3: 5, 4:5, 6: 99, 7: 89, 8:99, 9:89}

TABLE_NAME = 'groups_temp'


def get_connect():
    conn = psycopg2.connect(database="sharding", user="postgres", password="soraru11",
                            host="127.0.0.1", port="5432")
    return conn


# 读取用于测试的交易（此种方法对数据库资源占用极大）
def get_new_txs(limit, offset):
    res = []
    try:
        conn = get_connect()
        cursor = conn.cursor()
        # 注意: 要保证查询集是按tx_id顺序的
        cursor.execute('SELECT DISTINCT tx_id FROM txtest ORDER BY tx_id LIMIT {}'.format(limit))
        txs = cursor.fetchall()             # [(txid1), (txid2) ...]
        for tx_id in txs:
            cursor.execute('SELECT * FROM txtest WHERE tx_id = {}'.format(tx_id[0]))
            results = cursor.fetchall()     # [(txid1, in1, out1), (txid1, ...), (txid2 ...)]
            for r in results:
                res.append(r)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return res

    #return ((123, 2, 3), (123, 3, 5), (123, 2, 5),(125, 7, 9), (126, 8, 3))


# 读取用于测试的交易集（快速版，不精确设置输入多少条交易）
def get_new_txs_fast():
    try:
        conn = get_connect()
        cursor = conn.cursor()
        # 注意: 要保证查询集是按tx_id顺序的
        cursor.execute('SELECT * FROM txtest ORDER BY tx_id')
        results = cursor.fetchall()     # [(txid1, in1, out1), (txid1, ...), (txid2 ...)]
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return results


# 根据 addressId 查询 groupId，不存在返回-1
def get_group_id(addr_id):
    """
    group_id = groups.get(addr_id)
    if not group_id:
        return -1
    return group_id
    """
    sql = 'SELECT groupid FROM {} WHERE addressid = {}'.format(TABLE_NAME, addr_id)
    try:
        conn = get_connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
    except Exception as e:
        print(e)
    else:
        if result:
            res = result[0]
        else:
            res = -1
    finally:
        cursor.close()
        conn.close()

    return res


# 向分组索引表中插入新的地址
def insert_new_tx(addr_id, group_id):
    sql = 'INSERT INTO {} (addressid, groupid) VALUES ({}, {})'.format(TABLE_NAME, addr_id, group_id)
    try:
        conn = get_connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
        if conn:
            conn.rollback()
    finally:
        cursor.close()
        conn.close()
    return 0


if __name__ == '__main__':
    print(get_group_id(1396600))
    insert_new_tx(99999999, 77)
    print(get_new_txs(100))


