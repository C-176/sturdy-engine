# coding=gbk
import numpy as np
import pandas as pd


# Z-score原则
def ZScore(i, data, data_orig, index, threshold=3):
    data_d = np.array(data)
    mean_d = np.mean(data_d)
    print(i,'均值：',mean_d)
    std_d = np.std(data_d)
    outliers = []
    if i == '水源地原水浊度' or i == '进厂原水浊度' :
        threshold = 4
    for index_last, y in enumerate(data_d):
        z_score = (y - mean_d) / std_d
        if np.abs(z_score) > threshold  or y < 0:
            outliers.append(y)
            data_orig.iloc[index_last,index] = str(mean_d)
    return outliers,data_orig

# 数据清洗
def data_clean():
    number = 0
    while number < 3:  # 3为数据处理的次数
        data_orig = pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\baiyangwancorr.csv', index_col=None))
        print(data_orig.columns)
        for index, i in enumerate(data_colu_test):
            data_d = data_orig[i]
            index += 3

            # Z-score法则
            list, data_orig = ZScore(i, data_d, data_orig, index)

        try:
            data_orig.to_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\baiyangwancorr.csv', index=False)
        finally:
            print(f'第{number + 1}次数据清洗完毕！')

        number += 1


# 基于参数相关性的异常检测的模型系数返回
def para_corelation(colu1,colu2):
    """
    para:colu1:x,colu2:y
    return:k,b
    """
    data_d = pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\baiyangwancorr.csv', index_col=None),
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

data_colu_test = ['水源地原水浊度', '水源地耗氧量', '水源地PH值', '水源地水温',
       '水源地氨氮量', '水源地溶解氧', '水源地藻密度', '水源地电导率', '进厂原水浊度', '1200进厂水量',
       '1400进厂水量', '2号沉淀池进水水量', '2号沉淀池出水浊度']
data_colu = ['水源地原水浊度', '水源地耗氧量', '水源地PH值', '水源地水温',
       '水源地氨氮量', '水源地溶解氧', '水源地藻密度', '水源地电导率', '进厂原水浊度', '1200进厂水量',
       '1400进厂水量', '2号沉淀池进水水量', '2号沉淀池出水浊度', '2号矾投加量', '进厂1#加氯点投加量',
       '进厂2#加氯点投加量', '水源地1#加氯点投加量', '水源地2#加氯点投加量', '进厂臭氧预投加量']
# 数据清洗
data_clean()

# 开始分析相关性
data_colu1 = data_colu_test
data_colu2 = data_colu1.copy()
data_d = pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\baiyangwancorr.csv', index_col=None),index=None)

# 相关性(OK)
corr_dict = {}  # 存放相关系数数据
k_dict ={}
b_dict = {}
k2_dict ={}
b2_dict = {}
name_list = []  # 存放可以构成一定线性关系的元素名字
for index1, colu1 in enumerate(data_colu1):
    for index2, colu2 in enumerate(data_colu2):
        if colu1 != colu2:
            a = data_d[colu1]
            b = data_d[colu2]
            # print(a.mean())
            xie = a.cov(b)  # 协方差
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
# inxx = 0
for name in data_colu:  # 开始找出相关系数最大的每个组合。
    print(name)
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

        print(f'{list111[max_index]}之间的相关系数为{list222[max_index]}')
        print(f'{list111[max_index]}之间的线性关系是：y = {k:.6f}x+{b:.6f}')
        print('='*20)
    else:  # 如果没有元素与之构成线性关系，那就没辙了，直接利用基于正态分布的统计方法Z-Score方法进行异常检测。
        # 加载原始数据
        data_orig = pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\baiyangwancorr.csv', index_col=None))
        for index, i in enumerate(data_colu):
            if name == i:
                data_d = data_orig[name]  # 取出这一列元素
                index += 3  # 数据库中除了data_colu中的表头外，最开头还有三个表头，分别是id，日期，时间，这些对于数据预测没用，故index都得往后移3。
                # Z-socre法则
                list, data_orig = ZScore(i, data_d, data_orig, index)
                if len(list):  # 有值的话
                    error_dict2[name] = list  # 存到列表中
# 保存模型参数
data_df = pd.DataFrame({'对象':object_list,'k':k_list,'b':b_list})
data_df.to_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\线性模型.csv')

# 加载检测数据
check_df =  pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\baiyangwan.csv', index_col=None))
check_df = check_df.drop(columns=['id','水源地测量日期','水源地测量时间'])  # 剔除没必要检测的数据
#
# 将两个列表合并并去重并返回
def deleteExisted(list1,list_obj):
    for i in list1:
        if i not in list_obj:
            list_obj.append(i)
    return list_obj
# 对应的表头及阈值字典

threshold_dict1 = {'水源地原水浊度':1000, '水源地耗氧量':5, '进厂原水浊度':700, '水源地PH值':1, '水源地溶解氧':0.5, '水源地水温':5,
                   '1200进厂水量':150, '1400进厂水量':150, '2号沉淀池进水水量':50}


inxx = 0
for colu in data_colu:
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
        try:
            value = (y_test-b)/x_test - k  # 值计算  # RuntimeWarning: divide by zero encountered in true_divide
        except:
            print('')

        data_show = np.concatenate((y_test.reshape(-1,1),x_test.reshape(-1,1),value.reshape(-1,1)),axis=1)  # 把因变量，自变量，判断依据转维然后拼接
        errorThreshold = threshold_dict1[y]  # 设置阈值

        # data_get = np.concatenate((data_show[abs(data_show[:,-1])>abs(k*errorThreshold)],data_show[data_show[:,2] == None]),axis=0)  # 根据阈值筛选异常值
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

# TODO:将获得的异常数据或者模型进行应用，并与离群异常数据比较。