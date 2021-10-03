# coding=gbk
import numpy as np
import pandas as pd


# Z-scoreԭ��
def ZScore(i, data, data_orig, index, threshold=3):
    data_d = np.array(data)
    mean_d = np.mean(data_d)
    print(i,'��ֵ��',mean_d)
    std_d = np.std(data_d)
    outliers = []
    if i == 'ˮԴ��ԭˮ�Ƕ�' or i == '����ԭˮ�Ƕ�' :
        threshold = 4
    for index_last, y in enumerate(data_d):
        z_score = (y - mean_d) / std_d
        if np.abs(z_score) > threshold  or y < 0:
            outliers.append(y)
            data_orig.iloc[index_last,index] = str(mean_d)
    return outliers,data_orig

# ������ϴ
def data_clean():
    number = 0
    while number < 3:  # 3Ϊ���ݴ���Ĵ���
        data_orig = pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\PythonԴ��\06_���ѧϰ\RF\csv\baiyangwancorr.csv', index_col=None))
        print(data_orig.columns)
        for index, i in enumerate(data_colu_test):
            data_d = data_orig[i]
            index += 3

            # Z-score����
            list, data_orig = ZScore(i, data_d, data_orig, index)

        try:
            data_orig.to_csv(r'C:\Users\1\Desktop\PythonԴ��\06_���ѧϰ\RF\csv\baiyangwancorr.csv', index=False)
        finally:
            print(f'��{number + 1}��������ϴ��ϣ�')

        number += 1


# ���ڲ�������Ե��쳣����ģ��ϵ������
def para_corelation(colu1,colu2):
    """
    para:colu1:x,colu2:y
    return:k,b
    """
    data_d = pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\PythonԴ��\06_���ѧϰ\RF\csv\baiyangwancorr.csv', index_col=None),
                              index=None)
    data1 = data_d[colu1]
    data2 = data_d[colu2]
    data1_array = np.array(data1)
    data2_array = np.array(data2)
    data1_mean = data1_array.mean()
    data2_mean = data2_array.mean()

    a = data1_array*data2_array
    b = (data2_mean-data1_mean)*len(data1_array)
    c =data1_array.std()*len(data1_array)
    d = data2_array.std()*len(data2_array)
    k = (a-b).sum()/(c*d)
    b = data2_mean - k*data1_mean

    return k,b

data_colu_test = ['ˮԴ��ԭˮ�Ƕ�', 'ˮԴ�غ�����', 'ˮԴ��PHֵ', 'ˮԴ��ˮ��',
       'ˮԴ�ذ�����', 'ˮԴ���ܽ���', 'ˮԴ�����ܶ�', 'ˮԴ�ص絼��', '����ԭˮ�Ƕ�', '1200����ˮ��',
       '1400����ˮ��', '2�ų���ؽ�ˮˮ��', '2�ų���س�ˮ�Ƕ�']
data_colu = ['ˮԴ��ԭˮ�Ƕ�', 'ˮԴ�غ�����', 'ˮԴ��PHֵ', 'ˮԴ��ˮ��',
       'ˮԴ�ذ�����', 'ˮԴ���ܽ���', 'ˮԴ�����ܶ�', 'ˮԴ�ص絼��', '����ԭˮ�Ƕ�', '1200����ˮ��',
       '1400����ˮ��', '2�ų���ؽ�ˮˮ��', '2�ų���س�ˮ�Ƕ�', '2�ŷ�Ͷ����', '����1#���ȵ�Ͷ����',
       '����2#���ȵ�Ͷ����', 'ˮԴ��1#���ȵ�Ͷ����', 'ˮԴ��2#���ȵ�Ͷ����', '��������ԤͶ����']
# ������ϴ
data_clean()

# ��ʼ���������
data_colu1 = data_colu_test
data_colu2 = data_colu1.copy()
data_d = pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\PythonԴ��\06_���ѧϰ\RF\csv\baiyangwancorr.csv', index_col=None),index=None)

# �����(OK)
corr_dict = {}  # ������ϵ������
k_dict ={}
b_dict = {}
k2_dict ={}
b2_dict = {}
name_list = []  # ��ſ��Թ���һ�����Թ�ϵ��Ԫ������
for index1, colu1 in enumerate(data_colu1):
    for index2, colu2 in enumerate(data_colu2):
        if colu1 != colu2:
            a = data_d[colu1]
            b = data_d[colu2]
            # print(a.mean())
            xie = a.cov(b)  # Э����
            corr = a.corr(b)  # ���ϵ��
            if abs(corr) >= 0.4:  # ���ϵ������ֵ����0.4����Ϊ����Ԫ�ؾ���һ������������ԡ�0.4�������Թ�ϵ�������쳣���ǳ��������С�
                if colu1 not in name_list:
                    name_list.append(colu1)
                if colu2 not in name_list:
                    name_list.append(colu2)
                key1 = (colu1, colu2)
                corr_dict[key1] = corr
                k1,b1= para_corelation(colu1,colu2)  # para_corelation(x,y)
                k2,b2= para_corelation(colu2,colu1)  # para_corelation(y,x)  # �ֱ��������Ԫ�ظ�Ϊ�Ա������������k��b��
                k_dict[key1] = k1
                b_dict[key1] = b1
                k2_dict[key1] = k2
                b2_dict[key1] = b2

                # print('%s��%s��Э����Ϊ��%.4f,���ϵ��Ϊ��%.4f [�����]' % (colu1, colu2, xie, xishu))

    data_colu2.remove(colu1)  # ���Ѿ���������Ԫ���޳����������ظ���


# import operator

# sort_value_dic_instance = dict(sorted(corr_dict.items(), key=operator.itemgetter(1),reverse=True))  #����keyֵ����
# print(sort_value_dic_instance)   # �������������ϵ���ֵ䰴�����ϵ����С����һ�£���������û��Ҫ��

object_list = []  # �������ȷ����Ԫ�ض�
k_list = []  # �������ȷ����k
b_list = []  # �������ȷ����b
name_0_list = []
print('='*20)
error_dict2 ={}  # ����쳣ֵ�б�
index_list = []
# inxx = 0
for name in data_colu:  # ��ʼ�ҳ����ϵ������ÿ����ϡ�
    print(name)
    if name in name_list:  # ˵�����Թ������Թ�ϵ
        list111 = []  # ���Ԫ�ض�
        list222 = []  # ���Ԫ�ضԶ�Ӧ�����ϵ��
        for index,i in enumerate(corr_dict):
            # �ж����ϵ���ֵ���key��Ԫ���е�λ��
            if name == i[1]: #��nameΪ�������
                list111.append(i)
                list222.append(corr_dict[i])
        if len(list111) == 0:  # ˵�����Ԫ����Ԫ���е�0λ��
            for index, i in enumerate(corr_dict):
                if name == i[0]:
                    name_0_list.append(name)
                    list111.append(i)
                    list222.append(corr_dict[i])
        max_index = np.array(list222).argmax()  # ����������ϵ��������ֵ
        if name == list111[max_index][0]:
            k = k2_dict[list111[max_index]]
            b = b2_dict[list111[max_index]]
        else:
            k =  k_dict[list111[max_index]]
            b =  b_dict[list111[max_index]]

        object_list.append(list111[max_index])  # ���Ԫ�ض�

        k_list.append(k)  # ��Ŷ�Ӧk
        b_list.append(b)  # ��Ŷ�Ӧb
        # ���ˣ�ÿ��Ԫ�أ����������Ԫ�ظ����ɹ������Թ�ϵ����Ψһ�Ķ�Ӧ��������Թ�ϵ��k��b

        print(f'{list111[max_index]}֮������ϵ��Ϊ{list222[max_index]}')
        print(f'{list111[max_index]}֮������Թ�ϵ�ǣ�y = {k:.6f}x+{b:.6f}')
        print('='*20)
    else:  # ���û��Ԫ����֮�������Թ�ϵ���Ǿ�û���ˣ�ֱ�����û�����̬�ֲ���ͳ�Ʒ���Z-Score���������쳣��⡣
        # ����ԭʼ����
        data_orig = pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\PythonԴ��\06_���ѧϰ\RF\csv\baiyangwancorr.csv', index_col=None))
        for index, i in enumerate(data_colu):
            if name == i:
                data_d = data_orig[name]  # ȡ����һ��Ԫ��
                index += 3  # ���ݿ��г���data_colu�еı�ͷ�⣬�ͷ����������ͷ���ֱ���id�����ڣ�ʱ�䣬��Щ��������Ԥ��û�ã���index����������3��
                # Z-socre����
                list, data_orig = ZScore(i, data_d, data_orig, index)
                if len(list):  # ��ֵ�Ļ�
                    error_dict2[name] = list  # �浽�б���
# ����ģ�Ͳ���
data_df = pd.DataFrame({'����':object_list,'k':k_list,'b':b_list})
data_df.to_csv(r'C:\Users\1\Desktop\PythonԴ��\06_���ѧϰ\RF\csv\����ģ��.csv')

# ���ؼ������
check_df =  pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\PythonԴ��\06_���ѧϰ\RF\csv\baiyangwan.csv', index_col=None))
check_df = check_df.drop(columns=['id','ˮԴ�ز�������','ˮԴ�ز���ʱ��'])  # �޳�û��Ҫ��������
#
# �������б�ϲ���ȥ�ز�����
def deleteExisted(list1,list_obj):
    for i in list1:
        if i not in list_obj:
            list_obj.append(i)
    return list_obj
# ��Ӧ�ı�ͷ����ֵ�ֵ�

threshold_dict1 = {'ˮԴ��ԭˮ�Ƕ�':1000, 'ˮԴ�غ�����':5, '����ԭˮ�Ƕ�':700, 'ˮԴ��PHֵ':1, 'ˮԴ���ܽ���':0.5, 'ˮԴ��ˮ��':5,
                   '1200����ˮ��':150, '1400����ˮ��':150, '2�ų���ؽ�ˮˮ��':50}


inxx = 0
for colu in data_colu:
    if colu in name_list:
        y =colu  # Ԫ�أ�Ҳ�������
        a = data_df['����'][inxx]  # ����Ԫ�ص�Ԫ�ض�

        if y not in name_0_list:
            x = a[0]
        else:
            x = a[1]

        y_test = np.array(check_df[y])  # �����
        x_test = np.array(check_df[x])  # �Ա���
        # print(f'y:{y},x:{x}')
        k = data_df['k'][inxx]
        b = data_df['b'][inxx]
        inxx += 1
        try:
            value = (y_test-b)/x_test - k  # ֵ����  # RuntimeWarning: divide by zero encountered in true_divide
        except:
            print('')

        data_show = np.concatenate((y_test.reshape(-1,1),x_test.reshape(-1,1),value.reshape(-1,1)),axis=1)  # ����������Ա������ж�����תάȻ��ƴ��
        errorThreshold = threshold_dict1[y]  # ������ֵ

        # data_get = np.concatenate((data_show[abs(data_show[:,-1])>abs(k*errorThreshold)],data_show[data_show[:,2] == None]),axis=0)  # ������ֵɸѡ�쳣ֵ
        data_get = data_show[abs(data_show[:,-1])>abs(k*errorThreshold)]
        if y in error_dict2.keys():
            error_dict2[y] = deleteExisted(error_dict2[y],data_get[:,0].tolist())

        else:
            error_dict2[y] = data_get[:,0].tolist()
        if x in error_dict2.keys():
            error_dict2[x] = deleteExisted(error_dict2[y],data_get[:,1].tolist())
        else:
            error_dict2[x] = data_get[:, 1].tolist()
        # print(data_get,data_get.shape)
for i in error_dict2.keys():
    print(i)
    print(error_dict2[i],len(error_dict2[i]))

# TODO:����õ��쳣���ݻ���ģ�ͽ���Ӧ�ã�������Ⱥ�쳣���ݱȽϡ�