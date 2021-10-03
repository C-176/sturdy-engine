import datetime
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
import pydotplus
from IPython.display import Image, display
import sklearn.tree as tree
import joblib
# 设置绘图大小
# plt.style.use({'figure.figsize':(25,20)})

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

start_time = time.time()
x = pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\data_data.csv')
y = pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\data_target.csv')
# print(x.info())
print(x.head(1))
print(y.head(1))
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4,random_state=9999)  # 划分数据集


# K——Fold
# 加载RFR模型对象
para_grid = {
    'n_estimators': [5, 10, 20, 50, 100, 200],
    'max_depth': [3, 5, 7, 10],
    'max_features': [0.5, 0.55,0.6,0.65, 0.7]
}
RF = RandomForestRegressor()
# 导入网络搜索交叉验证，网络搜索可以让模型参数按照我们给定的列表遍历，找到效果最好的模型
# 交叉验证可以告诉我们模型的准确性
grid = GridSearchCV(RF, para_grid, cv=3)  # 交叉验证，3层
y_train = np.array(y_train).reshape(len(y_train), )  # 转化标签张量的维度
grid.fit(x_train, y_train)  # 训练
RF_para = grid.best_params_  # 获取最优参数
RF = grid.best_estimator_  # 选择最优随机森林
print('获得最优参数:', RF_para)  # 打印RF参数
# 可视化决策树
estimator = RF.estimators_[3]  # 选择第三个决策树供可视化
dot_data = tree.export_graphviz(estimator, out_file=None, filled=True, rounded=True)
graph = pydotplus.graph_from_dot_data(dot_data)
img = Image(graph.create_png())  # 生成图
graph.write_png(r"C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\3#决策树可视化.png")  # 存图

# 特征重要性可视化
feature_importances = RF.feature_importances_
# print(feature_importances)
feature_names = x_train.columns
important_indices = np.argsort(feature_importances)  # 返回升序排序的索引值到一个列表中

print('特征排序')  # 输出各特征重要性
for index in important_indices:
    print('%s' % feature_names[index], '\t', '%f' % feature_importances[index])

# 特征重要性排序
plt.figure(figsize=(7, 5))
plt.title('RF中不同特征的重要程度')
plt.bar(range(len(feature_importances)), feature_importances[important_indices], color='b')
plt.xticks(range(len(feature_importances)), np.array(feature_names)[important_indices], color='b')
plt.show()

# RF = RF.fit(x_train,y_train)  # 导入训练集
# RF_result = RF.predict(x_test)  # 获取测试结果
# print(RF_result)   # 打印测试结果

# 加载模型，不同的模型框架
RF2 = tree.DecisionTreeRegressor()  # 加载RFR对象
RF2 = RF2.fit(x_train, y_train)
RF_result2 = RF2.predict(x_test)
joblib.dump(RF_result2,filename=r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\RF2.m')

end_time = time.time()  # 模型训练与测试所耗时间

list1 = y_test.values.tolist()  # 将测试集的标签张量转化为列表，供画图。   list1形如：[[48],[49],[50]]
y_test = [i[0] for i in list1]  # 转化为 形如[48,49,50]
# # 可视化测试集上回归预测的结果
RF_result = RF.predict(x_test)
joblib.dump(RF_result,filename=r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\RF.m')

# 画图
result = {"Labels": y_test, "Prediction": RF_result}
result = pd.DataFrame(result)
# print(result.head(2))  # 可查看具体预测值
result['Labels'].plot(style='k*', figsize=(15, 5))
result['Prediction'].plot(style='r.')
plt.legend(fontsize=15, markerscale=3)  # 设置图例字号以及图例大小
plt.tick_params(labelsize=15)  # 设置坐标数字大小
plt.grid()

# 画图
x = range(len(list1))
plt.figure()  # 类似于先声明一张图片，这个figure后面所有的设置都是在这张图片上操作的
plt.plot(x, list1, color='black')  # 制图
plt.plot(x, RF_result, color='red', linestyle='--')  # 1#RFR的回归值
# plt.plot(x, RF_result2, color='green', linestyle='dashdot')  # 2#RFR的回归值
plt.show()  # 显示图片

# 计算均方误差和均方根误差
from sklearn import metrics
MSE = metrics.mean_squared_error(np.array(y_test).reshape(-1,1), RF_result)
R2 = metrics.r2_score(np.array(y_test).reshape(-1,1),RF_result)
RMSE = np.sqrt(MSE)
print('(MSE,RMSE,R2)=',(MSE, RMSE, R2))
# 保存数据
RF_result = {"矾量预测": RF_result}
result = pd.DataFrame(RF_result)
write_path = r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\矾量预测.csv'
result.to_csv(write_path,index_label='id')
print('用时:', datetime.timedelta(seconds=(end_time - start_time) // 1))  # 打印用时
