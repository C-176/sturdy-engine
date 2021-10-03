import numpy as np
import pandas as pd
import matrixprofile as mp
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def paint_single(col, data, num):
    list = []
    for i in data.tolist():
        # data = [x for x in i[0]]
        list.append(i)
    # plt.xlabel(col)

    plt.figure(figsize=(20, 14), dpi=100)  # 设置画布大小，像素
    plt.scatter(range(len(list)), list, label=f'{col}')
    plt.legend()  # 显示图片中的标签
    plt.savefig(rf'C:\Users\1\Pictures\Saved Pictures\scatter{num}.jpg')  # 保存图片

    plt.show()


data_colu = ['水源地原水浊度', '水源地耗氧量', '水源地PH值', '水源地水温',
             '水源地氨氮量', '水源地溶解氧', '水源地藻密度', '水源地电导率', '进厂原水浊度', '1200进厂水量',
             '1400进厂水量', '2号沉淀池进水水量', '2号沉淀池出水浊度', '2号矾投加量', '进厂1#加氯点投加量',
             '进厂2#加氯点投加量', '水源地1#加氯点投加量', '水源地2#加氯点投加量', '进厂臭氧预投加量']

# 开始分析相关性

data_d = pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\csv_last_lake0.csv', index_col=None),
                      index=None)
# for index, i in enumerate(data_colu):
#     paint_single(i, data_d[i], index)

'''
plt.legend（）函数主要的作用就是给图加上图例，plt.legend([x,y,z……])里面的参数使用的是list的的形式将图表的的名称喂给这个函数。
'''
data1 = data_d['进厂原水浊度']
data2 = data_d['水源地原水浊度'].tolist()
# data3 = data_d['水源地藻密度'].tolist()
x1 = range(len(data1))
x2 = range(len(data2))

plt.plot(x1, data1)
plt.plot(x2, data2)
# plt.plot(x2, data3)

plt.legend(['水源地原水浊度', '进厂原水浊度'])
plt.show()
