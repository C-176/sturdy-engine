# coding=gbk
import numpy as np
import pandas as pd
import matrixprofile as mp
import os


# Z-score原则
def detect1_outliers(i,data,data_orig,threshold=3):
    data_d = np.array(data)
    mean_d = np.mean(data_d)
    print(i,'均值：',mean_d)
    std_d = np.std(data_d)
    outliers = []
    if i == '原水浊度' or i == '进厂浊度':
        threshold = 5
    for index_last, y in enumerate(data_d):
        z_score = (y - mean_d) / std_d
        if np.abs(z_score) > threshold  or y < 0:
            outliers.append(y)
            data_orig.iloc[index_last,index] = str(mean_d)
    return outliers,data_orig

# IQR方法检测
def detect2_outliers(data):
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    iqr = q3 - q1  # Interquartile range
    fence_low = q1 - 1.5 * iqr
    fence_high = q3 + 1.5 * iqr
    outliers = data.loc[all(data.values < fence_low) or (data.values > fence_high)]
    return outliers

# matrixprofile 方法
def detect3_putliers(data_d):
    data_d = np.array(data_d)
    profile1 = mp.compute(data_d, windows=100, n_jobs=8)  # window_size为子序列长度
    discords = mp.discover.discords(profile1, k=10)  # k=1表示找到最大的那一个mp
    start_index = discords['discords'][0]  # 此时，这个子序列的起始点为start_index
    map_list = discords['mp']
    ts_list = discords['data']['ts']
    print( map_list,ts_list)



data_colu = ['原水浊度', '原水耗氧量', '原水PH值', '原水水温', '原水氨氮量', '原水溶解氧',
             '原水电导率', '进厂浊度', '1200进厂水量', '1400进厂水量', '2号沉淀池进水水量', '2号沉淀池出水浊度', '2号矾投加量',
              '1#加氯点投加量', '2#加氯点投加量', '原水1#加氯点投加量', '原水2#加氯点投加量', '臭氧预投加量', '藻密度']
num = 1
while(num <=5):
    data_orig = pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\baiyangwancorr.csv',index_col=None))
    # print(data_orig.columns)

    for index,i in enumerate(data_colu):
        data_d = data_orig[i]
        index += 3

        # (OK)36法则
        list, data_orig = detect1_outliers(i,data_d, data_orig)
        print(*list)

        # matrix profile(不好)
        # detect3_putliers(data_d)

        # matrix profile(不好)
        # detect3_putliers(data_d)

    try:
        # data_orig.index = range(1, len(data_orig) + 1)
        data_orig.to_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\baiyangwancorr.csv', index=False)
    finally:
        print('清洗所得数据写入完毕！')
    num +=1

#
#     # # IQR方法(效果不好，容易误判)
#     # data_d = pd.DataFrame(data_d,index=None)
#     # data_d = np.array(data_d)[:,0]
#     # data_d = pd.Series(data_d)
#     # error_data = detect2_outliers(data_d)
#     # print(i)
#     # print(*error_data)
#
# #
# # 开始分析相关性
# data_colu1 = data_colu
# data_colu2 = ['原水浊度', '原水耗氧量', '原水PH值', '原水水温', '原水氨氮量', '原水溶解氧',
#               '原水电导率', '进厂浊度', '1200进厂水量', '1400进厂水量', '2号沉淀池进水水量', '2号沉淀池出水浊度', '2号矾投加量', '1#加氯点投加量',
#               '2#加氯点投加量', '原水1#加氯点投加量', '原水2#加氯点投加量', '臭氧预投加量', '藻密度']
# data_d = pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\baiyangwancorr.csv', index_col=None),
#                           index=None)
# # 相关性(OK)
# corr_dict = {}
# for index1, colu1 in enumerate(data_colu):
#     for index2, colu2 in enumerate(data_colu2):
#
#         if colu1 != colu2:
#             a = data_d[colu1]
#             b = data_d[colu2]
#             # print(a.mean())
#             xie = a.cov(b)
#             xishu = a.corr(b)
#             if xishu > 0:
#                 key1 = '%s与%s' % (colu1, colu2)
#                 value1 = xishu
#                 corr_dict[key1] = value1
#                 # print('%s与%s的协方差为：%.4f,相关系数为：%.4f [正相关]' % (colu1, colu2, xie, xishu))
#     # print('*' * 150)
#     data_colu2.remove(colu1)
#     # print(*data_colu2)
#
# import operator
#
# sort_value_dic_instance = dict(sorted(corr_dict.items(), key=operator.itemgetter(1),reverse=True))  #按照key值升序
# # print(sort_value_dic_instance)
# print('\n相关性排名前二十：')
# for index,i in enumerate(sort_value_dic_instance):
#     word = '%s,%.4f' % (i,sort_value_dic_instance[i])
#     with open(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\参数相关系数.txt',mode='a',encoding='utf-8') as f:
#         f.write(word)
#         f.write('\n')
#     if index <= 19:
#         print(i,'%.4f' % sort_value_dic_instance[i])
