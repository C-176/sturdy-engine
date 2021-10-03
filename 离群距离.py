import random
import time

import pymysql
from dbutils.pooled_db import PooledDB
import numpy as np
# 读取数据库返回数据（db='test1'）
def query(sql):
    pool = PooledDB(pymysql, mincached=5, host='localhost', user='root', passwd='chenle123', db='test1',
                    port=3306)
    connection = pool.connection()
    cur = connection.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    connection.close()
    return result


# 离群距离
def out_instan(number,number_set):
    """
    number:滑动窗口中的子序列
    number_set:滑动窗口中的序列
    return:此子序列相对于整个窗口中序列的离群距离
    """
    number_list = []  # 建立一个列表供转为array
    for i in number_set:
        if i !='.':
            number_list.append(float(i))
    number_set1 = np.array(number_list)  # 整个滑动窗口序列转为array数组
    mul = len(number_set1)/len(number)   # 计算子序列复制多少倍可以与整个SW序列计算
    son_array = np.tile(np.array(number),(1,int(mul)))  # 在axis=0的方向扩张mul倍
    # print(len(number))
    # print(mul)
    # print(son_array.shape)
    # print(number_set1.shape)
    # 计算离群距离
    out_instance = np.mean(np.sqrt(sum(( son_array- number_set1) ** 2)/mul))

    return out_instance

sql = 'select * from baiyangwan'
result = query(sql)
# print(result)

data_colu = ['原水浊度', '原水耗氧量', '原水PH值', '原水水温', '原水氨氮量', '原水溶解氧',
                 '原水电导率', '进厂浊度', '1200进厂水量', '1400进厂水量', '2号沉淀池进水水量', '2号沉淀池出水浊度', '2号矾投加量',
                 '1#加氯点投加量', '2#加氯点投加量', '原水1#加氯点投加量', '原水2#加氯点投加量', '臭氧预投加量', '藻密度']
Tsm = []  # 多源序列数据列表
for index,colu in enumerate(data_colu):
    index += 3  # 数据库中除了data_colu中的表头外，最开头还有三个表头，分别是id，日期，时间，这些对于数据预测没用，故不提取。
    list = []
    for data in result:
        list.append(float(data[index]))
    Tsm.append(list)

# 对应的表头及阈值字典
threshold_dict = {'原水浊度':5.5, '原水耗氧量':0.2, '原水PH值':0.12, '原水水温':0.5, '原水氨氮量':0.03, '原水溶解氧':0.5,
                 '原水电导率':5.8, '进厂浊度':5.5, '1200进厂水量':7000, '1400进厂水量':7000, '2号沉淀池进水水量':10000, '2号沉淀池出水浊度':0.1, '2号矾投加量':2.,
                 '1#加氯点投加量':10, '2#加氯点投加量':10, '原水1#加氯点投加量':10, '原水2#加氯点投加量':10, '臭氧预投加量':0.1, '藻密度':70}

# 超参量
SW_SIZE = 2000  # 滑动窗口大小（Slide Window）
SON_SIZE = 10  # 子序列窗口大小

error_dict = {}  # 异常字典
for inx,key in enumerate(threshold_dict):
    out_list = []
    out_thresh = threshold_dict[key]  # 阈值
    i = Tsm[inx]  # 取单源序列数据
    print(key)
    for index in range(0,(len(i)-SW_SIZE),10):

        vi_index1 = 10

        vi = i[index:index+vi_index1]  # 子序列数据

        SW = i[index:index+SW_SIZE]  #   SW数据

        out_instance =out_instan(vi,SW)
        if out_instance > out_thresh :  # 若是离群距离大于阈值，增加到异常列表中。
            v1 = vi[0:5]
            out_instance1 = out_instan(v1, SW)
            if out_instance1 > out_thresh :

                for x in vi:
                    out_list.append(x)
            v2 = vi[6:]
            out_instance2 = out_instan(v2, SW)
            if out_instance1 > out_thresh :

                for x in vi:
                    out_list.append(x)
            # for x in vi:
            # i = TSm[0]
            # son_new_list = i[index-4+son_index+vi_index1:index+5+son_index+vi_index1]
            # for i in son_new_list:
            #     out_instance1 = out_instan(i,SW)
            #     if out_instance1 > out:
            #     out_list.append(x)

    error_dict[key] = out_list
    if out_list:  # 不为空的话
        print(*out_list)  # 打印全部元素
        print(f'异常数据总数：{len(out_list)}')
# TODO:把对应的异常列表保存，或直接比较。(已保存在error_dict字典中)
print("="*50)
print(len(error_dict))

