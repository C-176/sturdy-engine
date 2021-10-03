# coding=gbk
import numpy as np
import pandas as pd
import matrixprofile as mp
import os


# Z-scoreԭ��
def detect1_outliers(i,data,data_orig,threshold=3):
    data_d = np.array(data)
    mean_d = np.mean(data_d)
    print(i,'��ֵ��',mean_d)
    std_d = np.std(data_d)
    outliers = []
    if i == 'ԭˮ�Ƕ�' or i == '�����Ƕ�':
        threshold = 5
    for index_last, y in enumerate(data_d):
        z_score = (y - mean_d) / std_d
        if np.abs(z_score) > threshold  or y < 0:
            outliers.append(y)
            data_orig.iloc[index_last,index] = str(mean_d)
    return outliers,data_orig

# IQR�������
def detect2_outliers(data):
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    iqr = q3 - q1  # Interquartile range
    fence_low = q1 - 1.5 * iqr
    fence_high = q3 + 1.5 * iqr
    outliers = data.loc[all(data.values < fence_low) or (data.values > fence_high)]
    return outliers

# matrixprofile ����
def detect3_putliers(data_d):
    data_d = np.array(data_d)
    profile1 = mp.compute(data_d, windows=100, n_jobs=8)  # window_sizeΪ�����г���
    discords = mp.discover.discords(profile1, k=10)  # k=1��ʾ�ҵ�������һ��mp
    start_index = discords['discords'][0]  # ��ʱ����������е���ʼ��Ϊstart_index
    map_list = discords['mp']
    ts_list = discords['data']['ts']
    print( map_list,ts_list)



data_colu = ['ԭˮ�Ƕ�', 'ԭˮ������', 'ԭˮPHֵ', 'ԭˮˮ��', 'ԭˮ������', 'ԭˮ�ܽ���',
             'ԭˮ�絼��', '�����Ƕ�', '1200����ˮ��', '1400����ˮ��', '2�ų���ؽ�ˮˮ��', '2�ų���س�ˮ�Ƕ�', '2�ŷ�Ͷ����',
              '1#���ȵ�Ͷ����', '2#���ȵ�Ͷ����', 'ԭˮ1#���ȵ�Ͷ����', 'ԭˮ2#���ȵ�Ͷ����', '����ԤͶ����', '���ܶ�']
num = 1
while(num <=5):
    data_orig = pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\PythonԴ��\06_���ѧϰ\RF\csv\baiyangwancorr.csv',index_col=None))
    # print(data_orig.columns)

    for index,i in enumerate(data_colu):
        data_d = data_orig[i]
        index += 3

        # (OK)36����
        list, data_orig = detect1_outliers(i,data_d, data_orig)
        print(*list)

        # matrix profile(����)
        # detect3_putliers(data_d)

        # matrix profile(����)
        # detect3_putliers(data_d)

    try:
        # data_orig.index = range(1, len(data_orig) + 1)
        data_orig.to_csv(r'C:\Users\1\Desktop\PythonԴ��\06_���ѧϰ\RF\csv\baiyangwancorr.csv', index=False)
    finally:
        print('��ϴ��������д����ϣ�')
    num +=1

#
#     # # IQR����(Ч�����ã���������)
#     # data_d = pd.DataFrame(data_d,index=None)
#     # data_d = np.array(data_d)[:,0]
#     # data_d = pd.Series(data_d)
#     # error_data = detect2_outliers(data_d)
#     # print(i)
#     # print(*error_data)
#
# #
# # ��ʼ���������
# data_colu1 = data_colu
# data_colu2 = ['ԭˮ�Ƕ�', 'ԭˮ������', 'ԭˮPHֵ', 'ԭˮˮ��', 'ԭˮ������', 'ԭˮ�ܽ���',
#               'ԭˮ�絼��', '�����Ƕ�', '1200����ˮ��', '1400����ˮ��', '2�ų���ؽ�ˮˮ��', '2�ų���س�ˮ�Ƕ�', '2�ŷ�Ͷ����', '1#���ȵ�Ͷ����',
#               '2#���ȵ�Ͷ����', 'ԭˮ1#���ȵ�Ͷ����', 'ԭˮ2#���ȵ�Ͷ����', '����ԤͶ����', '���ܶ�']
# data_d = pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\PythonԴ��\06_���ѧϰ\RF\csv\baiyangwancorr.csv', index_col=None),
#                           index=None)
# # �����(OK)
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
#                 key1 = '%s��%s' % (colu1, colu2)
#                 value1 = xishu
#                 corr_dict[key1] = value1
#                 # print('%s��%s��Э����Ϊ��%.4f,���ϵ��Ϊ��%.4f [�����]' % (colu1, colu2, xie, xishu))
#     # print('*' * 150)
#     data_colu2.remove(colu1)
#     # print(*data_colu2)
#
# import operator
#
# sort_value_dic_instance = dict(sorted(corr_dict.items(), key=operator.itemgetter(1),reverse=True))  #����keyֵ����
# # print(sort_value_dic_instance)
# print('\n���������ǰ��ʮ��')
# for index,i in enumerate(sort_value_dic_instance):
#     word = '%s,%.4f' % (i,sort_value_dic_instance[i])
#     with open(r'C:\Users\1\Desktop\PythonԴ��\06_���ѧϰ\RF\csv\�������ϵ��.txt',mode='a',encoding='utf-8') as f:
#         f.write(word)
#         f.write('\n')
#     if index <= 19:
#         print(i,'%.4f' % sort_value_dic_instance[i])
