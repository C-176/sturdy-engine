import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

colums = ['id' ,'厂内日期','厂内时间', '水源地原水浊度', '水源地耗氧量', '水源地PH值', '水源地水温',
          '水源地氨氮量', '水源地溶解氧', '水源地藻密度', '水源地电导率', '进厂原水浊度', '1200进厂水量',
          '1400进厂水量', '2号沉淀池进水水量', '2号沉淀池出水浊度', '2号矾投加量', '进厂1#加氯点投加量',
          '进厂2#加氯点投加量', '水源地1#加氯点投加量', '水源地2#加氯点投加量', '进厂臭氧预投加量']

# 画图
def paint_single(col, data):
    list = []
    for i in data.tolist():
        list.append(i)
    plt.figure(figsize=(20, 14), dpi=100)  # 设置画布大小，像素
    plt.scatter(range(len(list)), list, label=f'{col}')
    plt.legend()  # 显示图片中的标签
    plt.show()

# 想要可视化的表头列表
data_colu = ['水源地原水浊度', '水源地耗氧量', '水源地PH值', '水源地水温',
             '水源地氨氮量', '水源地溶解氧', '水源地藻密度', '水源地电导率', '进厂原水浊度', '1200进厂水量',
             '1400进厂水量', '2号沉淀池进水水量', '2号沉淀池出水浊度', '2号矾投加量', '进厂1#加氯点投加量',
             '进厂2#加氯点投加量', '水源地1#加氯点投加量', '水源地2#加氯点投加量', '进厂臭氧预投加量']

# 加载测试数据
data_d = pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csvtest\baiyangwantest1.csv', index_col=None),
                      index=None)
# # 各个表头画图
# for i in data_colu:
#     paint_single(i, data_d[i])


data1 = data_d['进厂原水浊度'].tolist()
data2 = data_d['水源地原水浊度'].tolist()

# # 两浊度比较图
# x1 = range(len(data1))
# x2 = range(len(data2))
# plt.plot(x1, data1)
# plt.plot(x2, data2)
# plt.legend(['水源地原水浊度', '进厂原水浊度'])
# plt.show()

# columns_drop=['id', '厂内日期', '厂内时间','1200进厂水量', '1400进厂水量', '2号沉淀池进水水量',
#               '2号沉淀池出水浊度', '进厂1#加氯点投加量','进厂2#加氯点投加量', '水源地1#加氯点投加量',
#               '水源地2#加氯点投加量', '进厂臭氧预投加量']
columns_drop=['id', '厂内日期', '厂内时间','1200进厂水量', '1400进厂水量', '2号沉淀池进水水量','2号沉淀池出水浊度']

data_pd = pd.DataFrame(np.array(pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csvtest\baiyangwantest1.csv', index_col=None)), columns=colums)
data_data = data_pd.drop(columns=columns_drop, axis=1)
data_target = pd.DataFrame(data_pd['2号沉淀池出水浊度'], columns=['2号沉淀池出水浊度'])
data_target.index =  [i for i in range(1,len(data_data)+1)]

order1 = input('是否进行数据简单清洗？【Y/N】')
if order1 == 'Y':
    # 进行数据的简单清洗
    lista = []
    for i in range(len(data1) - 2):
        list1 = data1[i:i + 2]  # 小序列
        list2 = data2[i:i + 2]
        a = (list1[1] - list1[0])
        b = (list2[1] - list2[0])
        if a * b < 0 and (abs(a) / abs(b) > 2.5 or abs(a) / abs(b) < (1 / 2.5)):
            lista.append(i)

    list_id = [i for i in range(len(data1))]
    data_id = pd.DataFrame(list_id, columns=['ID'])

    data_d = pd.concat([data_id, data_d], axis=1)
    data_d = data_d[~data_d['ID'].isin(lista)].drop(columns='ID',axis=1)
    data_d.index = [i for i in range(1,len(data_d)+1)]
    # print(data_d)
    # data_target = data_target[~data_target['ID'].isin(lista)].drop(columns='ID',axis=1)

    data_data = data_d.drop(columns=columns_drop, axis=1)
    data_target = pd.DataFrame(data_d['2号沉淀池出水浊度'], columns=['2号沉淀池出水浊度'],)

# 开始加载模型并预测
model1 = joblib.load(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\RF.model')
# model2 = joblib.load(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\RF2.model')

RF1_result = model1.predict(data_data)
# RF2_result = model2.predict(data_data)

a = pd.concat([pd.DataFrame(RF1_result,index=[i for i in range(1,len(RF1_result)+1)]), data_target], axis=1)
print(a)
a.to_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csvtest\浊度预测结果')

MSE = metrics.mean_squared_error(data_target, RF1_result)
R21 = metrics.r2_score(data_target, RF1_result)


def R2(true, predict):
    data1_mean = np.mean(np.array(true))
    data11 = sum((np.array(true)- np.array(predict))**2)
    data22 = sum((np.array(true) - np.array(data1_mean))**2)
    R2 = 1 - (data22 / data11)

    return R2

# r2 = R2(data_target['2号沉淀池出水浊度'].tolist(), RF1_result)
# print(f'r2:{r2}')
# R22 = metrics.r2_score(np.array(data_target).reshape(-1, 1), RF2_result)
print(MSE,R21)

# 更新模型、重新预测
model1.fit(data_data,np.array(data_target).reshape(len(data_target),))

print(metrics.r2_score(model1.predict(data_data),data_target))
print(model1.score(data_data,data_target))


# 预测值可视化
data1 = data_target
data2 = RF1_result
# data3 = RF2_result
x1 = range(len(data1))
x2 = range(len(data2))

plt.plot(x1,data1)
plt.plot(x1,data2)
# plt.plot(x1,data3)
plt.legend(['真实','预测1'])
plt.show()


