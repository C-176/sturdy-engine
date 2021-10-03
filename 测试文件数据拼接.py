import datetime

import numpy as np
import pandas as pd
import pymysql
from dbutils.pooled_db import PooledDB

# 查询数据库
def query_read(sql):
    pool = PooledDB(pymysql, mincached=5, host='localhost', user='root', passwd='chenle123', db='test1',
                    port=3306)
    connection = pool.connection()
    cur = connection.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    connection.close()
    return result

# 写入数据
def query_write(sql):
    # 打开数据库连接
    db = pymysql.connect(user='root', passwd='chenle123', port=3306, database='test1', host='localhost')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 插入语句
    # sql = "update baiyangwan1 set 出水时间='%s'  where id = 3" % 'codetest'
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
        print('写入完毕!')
    except:
        # 发生错误时回滚
        db.rollback()
        print('回滚了')
    # 关闭数据库连接
    db.close()

# 进厂参数
def find_data(i, data, result, index_list):
    if 15 in index_list:
        # 出水日期:24 出水时间:25
        date_get = result[i][24]
        time_get = result[i][25]
    else:
        # 进厂日期:22 进厂时间:23
        date_get = result[i][22]
        time_get = result[i][23]

    date_str = date_get.isoformat()
    time_str = str(time_get)
    time_min = datetime.datetime.strptime(time_str, '%H:%M:%S').minute
    time_hour = datetime.datetime.strptime(time_str, '%H:%M:%S').hour
    # 插值原则
    time_before_str = f'{time_hour}:00:00'
    time_behind_str = f'{time_hour + 1}:00:00'

    sql1 = f"SELECT * FROM baiyangwantest WHERE 厂内日期='{date_str}' and 厂内时间='{time_before_str}' order by id DESC limit 1"
    sql2 = f"SELECT * FROM baiyangwantest WHERE 厂内日期='{date_str}' and 厂内时间='{time_behind_str}' order by id DESC limit 1"
    rate = time_min/60
    result1 = query_read(sql1)
    result2 = query_read(sql2)

    if len(result1) != 0 and len(result2) != 0:  # 可以插值
        for j in index_list:
            result_get = float(result1[0][j])+(float(result2[0][j])-float(result1[0][j]))*rate
            # print(data.iloc[i,index])
            # print(result1[0][j],result2[0][j],result_get)
            data.iloc[i,j]= result_get
    elif len(result1) == 0 and len(result2) != 0:  # 不能插值，有啥用啥吧
        for j in index_list:
            result_get = float(result2[0][j])
            data.iloc[i,j]= result_get
    elif len(result1) != 0 and len(result2) == 0:  # 不能插值，有啥用啥吧
        for j in index_list:
            result_get = float(result1[0][j])
            data.iloc[i,j]= result_get
    elif len(result1) == 0 and len(result2) == 0:  # 找不到与之对应的数据，要剔除，先作标记，给厂内时间这一列填入None
        data.iloc[i,2]= None

    return data

sql = f'select * from baiyangwantest'
result = query_read(sql)
data = pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csvtest\baiyangwantest.csv', index_col=None))
try:
    for index,i in enumerate(result):
        print(index,'---------------------')
        find_data(index, data, result, [3,4,5,6,7,8,9,10,19,20])
        data = find_data(index, data, result,[15])

finally:
    # 去掉时间一列有0值的行（非测量值经处理后为0）
    data = data.dropna(subset=[u'厂内时间'], inplace=False)  # 此处inplace不可改为True，否则输出None
    data.index = range(1,len(data)+1)
    data.to_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csvtest\baiyangwantest1.csv',index=False)
