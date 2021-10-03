import joblib
import numpy

model = joblib.load(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\RF.model')
list_test = [21.47266,2.841449,8.507033,9.804233,0.2186362,13.93,454.6829,24.0162,5560.0,6020.0,3150.0,8.793390774031133,35.87963,165.8854,0.0,0.0,0.4,357.25
]
print(len(list_test))
list_test = numpy.array(list_test).reshape(1,-1)
result_test = numpy.array(1.912616).reshape(-1,1)

print(model.predict(list_test))
# 重新设置模型参数并训练
model.fit(list_test,result_test)

#新模型做预测
print(model.predict(list_test))
# print(model.score(test_X,test_y))
