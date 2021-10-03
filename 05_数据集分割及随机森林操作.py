import datetime
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, KFold
from sklearn.ensemble import RandomForestRegressor
import pydotplus
from IPython.display import Image, display
import sklearn.tree as tree
import joblib
from sklearn import metrics

# 开始时刻
start_time = time.time()

# 这两个参数的默认设置都是False,这两行是为了让DataFrame对齐显示。
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
# 这两行为了让图像正常显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def train(data_pd, columns_drop,model_name):
    data_data = data_pd.drop(columns=columns_drop, axis=1)
    # # 权重
    # value = data_data['水源地原水浊度']*0.3+data_data['进厂原水浊度']*0.7
    # data_data = pd.concat([data_data,value],axis=1)
    # data_data = data_data.rename(columns={0:'加权浊度'}).drop(columns=['水源地原水浊度','进厂原水浊度'],axis=1)
    # print(data_data)
    data_target = pd.DataFrame(data_pd['2号沉淀池出水浊度'], columns=['2号沉淀池出水浊度'])

    # # 保存训练数据
    # data_target.to_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\data_target.csv', index=False, columns=None)
    # data_data.to_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\data_data.csv', index=False, columns=None)

    x = data_data
    y = data_target

    # 打印表头信息
    print(x.head(1))
    print(y.head(1))

    # 划分数据集
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)  # 划分数据集
    y_train = np.array(y_train).reshape(len(y_train), )  # 转化标签张量的维度
    y_test = np.array(y_test).reshape(len(y_test), )

    # 超参数列表待选
    para_grid = {
        'n_estimators': [50, 70, 100, 200],
        'max_depth': [3, 5, 7, 10],
        'max_features': [0.5, 0.6, 0.65, 0.7, 0.8]
    }

    # 加载RFR模型对象
    RF = RandomForestRegressor()

    # 导入网络搜索交叉验证，网络搜索可以让模型参数按照我们给定的列表遍历，找到效果最好的模型
    # 交叉验证可以告诉我们模型的准确性
    # K——Fold
    kFold = KFold(n_splits=10, shuffle=True)
    grid = GridSearchCV(RF, para_grid, cv=kFold, n_jobs=-1)  # 交叉验证，10层
    grid.fit(x_train, y_train, )  # 训练
    RF = grid.best_estimator_  # 选择最优模型
    RF1_para = grid.best_params_  # 获取最优参数
    print('获得最优参数:', RF1_para)  # 打印RF参数
    # 这个是单纯的K折交叉验证，上面的是把K折交叉验证和网格搜索合并使用了
    # score = cross_val_score(RF,x_train,y_train,cv=10)
    # print(score)
    # print(score.mean())

    # # 可视化决策树
    # estimator = RF.estimators_[3]  # 选择第三个决策树供可视化
    # dot_data = tree.export_graphviz(estimator, out_file=None, filled=True, rounded=True)
    # graph = pydotplus.graph_from_dot_data(dot_data)
    # img = Image(graph.create_png())  # 生成图
    # graph.write_png(r"C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\3#决策树可视化.png")  # 存图

    # 特征重要性可视化
    feature_importance = RF.feature_importances_
    # print(feature_importance)
    feature_names = x_train.columns
    important_indices = np.argsort(feature_importance)  # 返回升序排序的索引值到一个列表中
    print('特征排序')  # 输出各特征重要性
    for index in reversed(important_indices):
        print(f'{feature_names[index]}\t{feature_importance[index]}')

    # # 特征重要性排序画图
    # plt.figure(figsize=(20, 12))
    # plt.title('RF中不同特征的重要程度')
    # plt.bar(range(len(feature_importance)), feature_importance[important_indices], color='b')
    # plt.xticks(range(len(feature_importance)), np.array(feature_names)[important_indices], color='b')
    # plt.show()

    # # 加载不同的模型框架的模型：tree包下的
    # RF2 = tree.DecisionTreeRegressor()  # 加载RFR对象
    # RF2 = RF2.fit(x_train, y_train)
    # joblib.dump(RF2, filename=r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\RF2.model')
    # RF2_result = RF2.predict(x_test)

    # list1 = y_test.values.tolist()  # 将测试集的标签张量转化为列表，供画图。   list1形如：[[48],[49],[50]]
    # y_test = [i[0] for i in list1]  # 转化为 形如[48,49,50]
    # # 可视化测试集上回归预测的结果
    RF_result = RF.predict(x_test)
    # 保存模型
    joblib.dump(RF, filename=fr'C:\Users\1\Desktop\Python源码\06_深度学习\RF\{model_name}.model')

    # # 画图
    # result = {"Labels": y_test, "Prediction": RF_result}
    # result = pd.DataFrame(result)
    # # print(result.head(2))  # 可查看具体预测值
    # result['Labels'].plot(style='k*', figsize=(15, 5))
    # result['Prediction'].plot(style='r.')
    # plt.legend(fontsize=15, markerscale=3)  # 设置图例字号以及图例大小
    # plt.tick_params(labelsize=15)  # 设置坐标数字大小
    # plt.grid()

    # 画图
    x = range(len(y_test))
    plt.figure(figsize=(20, 14), dpi=100)  # 类似于先声明一张图片，这个figure后面所有的设置都是在这张图片上操作的
    plt.plot(x, y_test)  # 制图
    plt.plot(x, RF_result)  # 1#RFR的回归值
    plt.legend(['真实', '预测'])
    plt.show()  # 显示图片

    # 计算均方方差和R2
    MSE = metrics.mean_squared_error(y_test, RF_result)
    R2 = metrics.r2_score(y_test, RF_result)
    print('(MSE,R2)=', (MSE, R2))


# DataFrame完整表头
colums = ['id', '水源地原水浊度', '水源地耗氧量', '水源地PH值', '水源地水温',
          '水源地氨氮量', '水源地溶解氧', '水源地藻密度', '水源地电导率', '进厂原水浊度', '1200进厂水量',
          '1400进厂水量', '2号沉淀池进水水量', '2号沉淀池出水浊度', '2号矾投加量', '进厂1#加氯点投加量',
          '进厂2#加氯点投加量', '水源地1#加氯点投加量', '水源地2#加氯点投加量', '进厂臭氧预投加量']

# 加载数据，并指定表头
data_pd_lake0 = pd.DataFrame(
    np.array(pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\csv_last_lake0.csv', index_col=None)),
    columns=colums)
columns_drop_lake0 = ['id', '1200进厂水量', '1400进厂水量', '2号沉淀池出水浊度', '水源地1#加氯点投加量', '水源地2#加氯点投加量' ]
train(data_pd_lake0, columns_drop_lake0,'lake0')
data_pd_fact0 = pd.DataFrame(
    np.array(pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\csv_last_fact0.csv', index_col=None)),
    columns=colums)
columns_drop_fact0 = ['id', '1200进厂水量', '1400进厂水量', '2号沉淀池出水浊度', '进厂1#加氯点投加量', '进厂2#加氯点投加量']
train(data_pd_fact0, columns_drop_fact0,'fact0')
data_pd_no0 = pd.DataFrame(
    np.array(pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\csv_last.csv', index_col=None)), columns=colums)
columns_drop_no0 = ['id', '1200进厂水量', '1400进厂水量', '2号沉淀池出水浊度', ]
train(data_pd_no0, columns_drop_no0,'no0')
end_time = time.time()  # 结束时刻
print('用时:', datetime.timedelta(seconds=(end_time - start_time) // 1))  # 打印用时