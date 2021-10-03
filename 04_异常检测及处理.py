import pymysql
from dbutils.pooled_db import PooledDB
import numpy as np
import pandas as pd

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
    # 计算离群距离
    out_instance = np.mean(np.sqrt(sum(( son_array- number_set1) ** 2)/mul))

    return out_instance

print('离群距离---------------------------')
sql = 'select * from baiyangwancorr1'
result = query(sql)

data_colu_whole = ['水源地原水浊度', '水源地耗氧量', '水源地PH值', '水源地水温',
       '水源地氨氮量', '水源地溶解氧', '水源地藻密度', '水源地电导率', '进厂原水浊度', '1200进厂水量',
       '1400进厂水量', '2号沉淀池进水水量', '2号沉淀池出水浊度', '2号矾投加量', '进厂1#加氯点投加量',
       '进厂2#加氯点投加量', '水源地1#加氯点投加量', '水源地2#加氯点投加量', '进厂臭氧预投加量']


Tsm = []  # 多源序列数据列表
for index,colu in enumerate(data_colu_whole):
    index += 3  # 数据库中除了data_colu中的表头外，最开头还有三个表头，分别是id，日期，时间，这些对于数据预测没用，故不提取。
    list = []
    for data in result:
        list.append(float(data[index]))
    Tsm.append(list)

# 对应的表头及阈值字典
threshold_outdistance_dict = {'水源地原水浊度':6, '水源地耗氧量':0.4, '水源地PH值':1, '水源地水温':0.7,
                              '水源地氨氮量':0.05, '水源地溶解氧':0.21,'水源地藻密度':125,'水源地电导率':5.0,
'进厂原水浊度':5, '1200进厂水量':340, '1400进厂水量':370, '2号沉淀池进水水量':150, '2号沉淀池出水浊度':1.0,
'2号矾投加量':2, '进厂1#加氯点投加量':10, '进厂2#加氯点投加量':10, '水源地1#加氯点投加量':10, '水源地2#加氯点投加量':10,
'进厂臭氧预投加量':0.1}

# 超参量
SW_SIZE = 2000  # 滑动窗口大小（Slide Window）
SON_SIZE = 10  # 子序列窗口大小
error_dict1 = {}  # 异常字典

for inx,key in enumerate(threshold_outdistance_dict):

    out_list = []
    out_thresh = threshold_outdistance_dict[key]  # 阈值
    i = Tsm[inx]  # 取单源序列数据
    print(key)

    for index in range(0,(len(i)-SW_SIZE),10):

        vi_index1 = 10
        vi = i[index:index+vi_index1]  # 子序列数据
        SW = i[index:index+SW_SIZE]  #  SW数据
        out_instance =out_instan(vi,SW)

        if out_instance > out_thresh :  # 若是离群距离大于阈值，分成两半再检测一下。
            v1 = vi[0:5]  # 子序列的前一半
            out_instance1 = out_instan(v1, SW)
            if out_instance1 > out_thresh :
                for x in vi:
                    out_list.append(x)
            v2 = vi[6:]  # 子序列的后一半
            out_instance2 = out_instan(v2, SW)
            if out_instance1 > out_thresh :
                for x in vi:
                    out_list.append(x)

    error_dict1[key] = out_list
    if out_list:  # 不为空的话
        print(*sorted(out_list))  # 打印全部元素
        print(f'异常数据总数：{len(out_list)}')
# TODO:把对应的异常列表保存，或直接比较。(已保存在error_dict1字典中)



# Z-score原则
def ZScore(i, data, data_orig, index, threshold=3):
    data_d = np.array(data)
    mean_d = np.mean(data_d)
    # print(i,'均值：',mean_d)
    std_d = np.std(data_d)
    outliers = []
    for index_last, y in enumerate(data_d):
        z_score = (y - mean_d) / std_d
        if i in data_colu_test and y == 0:  # 不可能为0的元素挑出来
            outliers.append(y)
            data_orig.iloc[index_last, index] = str(mean_d)
        if np.abs(z_score) > threshold  or y < 0:  #
            outliers.append(y)
            data_orig.iloc[index_last,index] = str(mean_d)
    return outliers,data_orig

# 不用修改原数据的ZSscore检测
def ZScoreLast(data, threshold):
    data_d = np.array(data)
    mean_d = np.mean(data_d)
    std_d = np.std(data_d)
    outliers = []
    for index_last, y in enumerate(data_d):
        z_score = (y - mean_d) / std_d
        if i in data_colu_test and y == 0:  # 不可能为0的元素挑出来
            outliers.append(y)
        if np.abs(z_score) > threshold  or y < 0:
            outliers.append(y)
    return outliers

# 数据清洗
def data_clean():
    number = 0
    while number < 3:  # 3为数据处理的次数
        data_orig = pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\baiyangwancorr2.csv', index_col=None))

        for index, i in enumerate(data_colu_whole):
            data_d = data_orig[i]
            index += 3

            # Z-socre法则
            list, data_orig = ZScore(i, data_d, data_orig, index)

        data_orig.to_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\baiyangwancorr2.csv', index=False)
        print(f'第{number + 1}次数据清洗完毕！')
        number += 1


# 基于参数相关性的异常检测的模型系数返回
def para_corelation(colu1,colu2):
    """
    para:colu1:x,colu2:y
    return:k,b
    """
    data_d = pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\baiyangwancorr2.csv', index_col=None),
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

# 不可能为0的元素列表

data_colu_test = ['水源地原水浊度', '水源地耗氧量', '水源地PH值', '水源地水温',
       '水源地氨氮量', '水源地溶解氧', '水源地藻密度', '水源地电导率', '进厂原水浊度', '1200进厂水量',
       '1400进厂水量', '2号沉淀池进水水量', '2号沉淀池出水浊度']

# 数据清洗
# print('数据清洗---------------------------')
# data_clean()


# 开始分析相关性
print('基于线性关系---------------------------')
data_colu1 = data_colu_test
data_colu2 = data_colu1.copy()
data_d = pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\baiyangwancorr2.csv', index_col=None),index=None)

# 相关性(OK)
corr_dict = {}  # 存放相关系数数据
k_dict ={}
b_dict = {}
k2_dict ={}
b2_dict = {}
name_list = []  # 存放可以构成一定线性关系的元素名字

for colu1 in data_colu1:
    for colu2 in data_colu2:
        if colu1 != colu2:
            a = data_d[colu1]
            b = data_d[colu2]
            # xie = a.cov(b)  # 协方差
            corr = a.corr(b)  # 相关系数
            if abs(corr) >= 0.4:  # 相关系数绝对值大于0.4才认为两个元素具有一定的线性相关性。0.4以下线性关系过弱，异常检测非常容易误判。
                if colu1 not in name_list:
                    name_list.append(colu1)
                if colu2 not in name_list:
                    name_list.append(colu2)
                key1 = (colu1, colu2)
                corr_dict[key1] = corr
                k1,b1= para_corelation(colu1,colu2)  # para_corelation(x,y)
                k2,b2= para_corelation(colu2,colu1)  # para_corelation(y,x)  # 分别计算两个元素各为自变量与因变量的k与b。
                k_dict[key1] = k1
                b_dict[key1] = b1
                k2_dict[key1] = k2
                b2_dict[key1] = b2

                # print('%s与%s的协方差为：%.4f,相关系数为：%.4f [正相关]' % (colu1, colu2, xie, xishu))

    data_colu2.remove(colu1)  # 把已经遍历过的元素剔除掉，避免重复。


# import operator

# sort_value_dic_instance = dict(sorted(corr_dict.items(), key=operator.itemgetter(1),reverse=True))  #按照key值升序
# print(sort_value_dic_instance)   # 本来想把这个相关系数字典按照相关系数大小排序一下，后来发现没必要。

object_list = []  # 存放最终确定的元素对
k_list = []  # 存放最终确定的k
b_list = []  # 存放最终确定的b
name_0_list = []
print('='*20)
error_dict2 ={}  # 存放异常值列表
index_list = []

for name in data_colu_whole:  # 开始找出相关系数最大的每个组合。
    # print(name)
    if name in name_list:  # 说明可以构成线性关系
        list111 = []  # 存放元素对
        list222 = []  # 存放元素对对应的相关系数
        for index,i in enumerate(corr_dict):
            # 判断相关系数字典中key的元组中的位置
            if name == i[1]: #（name为因变量）
                list111.append(i)
                list222.append(corr_dict[i])
        if len(list111) == 0:  # 说明这个元素在元组中的0位置
            for index, i in enumerate(corr_dict):
                if name == i[0]:
                    name_0_list.append(name)
                    list111.append(i)
                    list222.append(corr_dict[i])
        max_index = np.array(list222).argmax()  # 返回最大相关系数的索引值
        if name == list111[max_index][0]:
            k = k2_dict[list111[max_index]]
            b = b2_dict[list111[max_index]]
        else:
            k =  k_dict[list111[max_index]]
            b =  b_dict[list111[max_index]]

        object_list.append(list111[max_index])  # 存放元素对
        k_list.append(k)  # 存放对应k
        b_list.append(b)  # 存放对应b
        # 至此，每个元素，如果有其它元素跟她可构成线性关系，则唯一的对应这最大线性关系的k与b

        # print(f'{list111[max_index]}之间的相关系数为{list222[max_index]}')
        # print(f'{list111[max_index]}之间的线性关系是：y = {k:.6f}x+{b:.6f}')
        # print('='*20)
    else:  # 如果没有元素与之构成线性关系，那就没辙了，直接利用基于正态分布的统计方法Z-Score方法进行异常检测。
        # 加载原始数据
        # print("=====",name)
        data_orig = pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\baiyangwancorr2.csv', index_col=None))
        for index, i in enumerate(data_colu_whole):
            if name == i:
                data_d = data_orig[name]  # 取出这一列元素
                # index += 3  # 数据库中除了data_colu中的表头外，最开头还有三个表头，分别是id，日期，时间，这些对于数据预测没用，故index都得往后移3。
                # Z-socre法则
                list = ZScoreLast(data_d,3)
                # if len(list):  # 有值的话
                error_dict2[name] = list  # 存到列表中
# 保存模型参数
data_df = pd.DataFrame({'对象':object_list,'k':k_list,'b':b_list})
data_df.to_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\线性模型.csv')

# 加载检测数据
print('加载原数据---------------------------')
check_df =  pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\baiyangwancorr1.csv', index_col=None))
check_df = check_df.drop(columns=['id','厂内日期','厂内时间'])  # 剔除没必要检测的数据
num1 = len(check_df)
# 将两个列表合并并去重并返回
def deleteExisted(list1,list_obj):
    for i in list1:
        if i not in list_obj:
            list_obj.append(i)
    return list_obj

threshold_dict1 = {'水源地原水浊度':1200, '水源地耗氧量':5, '进厂原水浊度':1200, '水源地PH值':5, '水源地溶解氧':1, '水源地水温':20,
                   '1200进厂水量':80, '1400进厂水量':150, '2号沉淀池进水水量':50,'水源地藻密度':500,'水源地氨氮量':1,'水源地电导率':500}

inxx = 0
for colu in data_colu_whole:
    if colu in name_list:
        y =colu  # 元素，也是因变量
        a = data_df['对象'][inxx]  # 包含元素的元素对
        if y not in name_0_list:
            x = a[0]
        else:
            x = a[1]
        y_test = np.array(check_df[y])  # 因变量
        x_test = np.array(check_df[x])  # 自变量
        # print(f'y:{y},x:{x}')
        k = data_df['k'][inxx]
        b = data_df['b'][inxx]
        inxx += 1

        value = (y_test-b)/x_test - k  # 值计算  # RuntimeWarning: divide by zero encountered in true_divide
        # 把因变量，自变量，判断依据转维然后拼接
        data_show = np.concatenate((y_test.reshape(-1,1),x_test.reshape(-1,1),value.reshape(-1,1)),axis=1)
        errorThreshold = threshold_dict1[y]  # 设置阈值

        data_get = data_show[abs(data_show[:,-1])>abs(k*errorThreshold)]
        if y in error_dict2.keys():
            error_dict2[y] = deleteExisted(error_dict2[y],data_get[:,0].tolist())
        else:
            error_dict2[y] = data_get[:,0].tolist()
        if x in error_dict2.keys():
            error_dict2[x] = deleteExisted(error_dict2[y],data_get[:,1].tolist())
        else:
            error_dict2[x] = data_get[:, 1].tolist()
    # print(colu,error_dict2[colu])


#
# 对应的表头及阈值字典
threshold_dict_last = {'水源地原水浊度':0.85, '水源地耗氧量':1.1, '水源地PH值':0.12, '水源地水温':5,
                       '水源地氨氮量':0.015, '水源地溶解氧':0.5, '水源地电导率':0.8, '进厂原水浊度':0.79,
                       '1200进厂水量':0.275, '1400进厂水量':0.485, '2号沉淀池进水水量':0.295, '2号沉淀池出水浊度':0.02,
                       '2号矾投加量':1.7, '进厂1#加氯点投加量':1, '进厂2#加氯点投加量':1, '水源地1#加氯点投加量':1,
                       '水源地2#加氯点投加量':1, '进厂臭氧预投加量':0.1, '水源地藻密度':2.5}
dict_mean = {'水源地原水浊度': 43.804107451746106, '水源地耗氧量': 2.6676340898689297, '水源地PH值': 7.980259768884892, '水源地水温': 16.760875336405874, '水源地氨氮量': 0.2053386873096523, '水源地溶解氧': 9.884565347721823, '水源地藻密度': 458.1864907975963, '水源地电导率': 411.8678551292491, '进厂原水浊度': 40.898314109787165, '1200进厂水量': 22090.789493405275, '1400进厂水量': 39827.78589628297, '2号沉淀池进水水量': 29636.021257905086, '2号沉淀池出水浊度': 1.2258663802002399}

for colum in data_colu_whole:
    # print(colum)
    error_dict1[colum] = deleteExisted(error_dict2[colum], error_dict1[colum])
    error_dict1[colum] = sorted(ZScoreLast(error_dict1[colum], threshold_dict_last[colum]))
    # print(*error_dict1[colum])
    # print(len(check_df))
    check_df = check_df[~check_df[colum].isin(error_dict1[colum])]  # 删除数据
    if colum in dict_mean.keys():
        check_df = check_df[~(check_df[colum]==dict_mean[colum])]  # 删除数据


# print(len(check_df))
# print(check_df)
# 根据水源地原水浊度与进厂原水浊度之间的关系最终剔除
data1 = check_df['水源地原水浊度'].tolist()
data2 = check_df['进厂原水浊度'].tolist()
lista = []
for i in range(len(data1)-2):
    list1 = data1[i:i + 2]  # 小序列
    list2 = data2[i:i + 2]
    a = (list1[1]-list1[0])
    b = (list2[1]-list2[0])
    if a*b<0 and (abs(a)/abs(b)>2.5 or abs(a)/abs(b)<(1/2.5)) :#
        lista.append(i)

list_id = [i for i in range(len(data1))]
data_id = pd.DataFrame(list_id,columns=['id'])
check_df.index = [i for i in range(len(check_df))]
check_df = pd.concat([data_id,check_df],axis=1)
check_df = check_df[~check_df['id'].isin(lista)]
num2 = len(check_df)

print(f'共剔除了{num1-num2}个，此步剔除了{len(lista)}个')
check_df = check_df.drop('id',axis=1)
# check_df.index = [i for i in range(len(check_df))]
# print(check_df)
csv_last_fact0 = check_df.loc[(check_df['进厂1#加氯点投加量']==0.0) & (check_df['进厂2#加氯点投加量']==0.0)]
csv_last_lake0 = check_df.loc[(check_df['水源地1#加氯点投加量']==0.0)&(check_df['水源地2#加氯点投加量']==0.0)]
csv_last = check_df.loc[(check_df['进厂1#加氯点投加量']!=0.0)&(check_df['进厂2#加氯点投加量']!=0.0)&(check_df['水源地1#加氯点投加量']!=0.0)&(check_df['水源地2#加氯点投加量']!=0.0)]
csv_last_fact0.index = range(len(csv_last_fact0))
csv_last_lake0.index = range(len(csv_last_lake0))
csv_last.index = range(len(csv_last))
print(csv_last_lake0)
print(csv_last_fact0)
print(csv_last)
check_df.index = range(1, len(check_df) + 1)
print(check_df)
csv_last_lake0.to_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\csv_last_lake0.csv',index_label='id')
csv_last_fact0.to_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\csv_last_fact0.csv',index_label='id')
csv_last.to_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\csv_last.csv',index_label='id')
# check_df.to_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\csv_last.csv',index_label='id')
