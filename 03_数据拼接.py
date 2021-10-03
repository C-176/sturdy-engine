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

    date_str = date_get.isoformat() # 准换为字符串
    time_str = str(time_get)
    time_min = datetime.datetime.strptime(time_str, '%H:%M:%S').minute
    time_hour = datetime.datetime.strptime(time_str, '%H:%M:%S').hour

    time_before_str = f'{time_hour}:00:00'
    time_behind_str = f'{time_hour + 1}:00:00'
    # 就近原则
    # if time_min >=30:
    #     time_str = f'{time_hour+1}:00:00'
    # else:
    #     time_str = f'{time_hour}:00:00'

    # 插值原则
    sql1 = f"SELECT * FROM baiyangwancorr WHERE 厂内日期='{date_str}' and 厂内时间='{time_before_str}' order by id DESC limit 1"
    sql2 = f"SELECT * FROM baiyangwancorr WHERE 厂内日期='{date_str}' and 厂内时间='{time_behind_str}' order by id DESC limit 1"
    rate = time_min/60
    result1 = query_read(sql1)
    result2 = query_read(sql2)

    if len(result1) != 0 and len(result2) != 0:  # 可以插值
        for j in index_list:
            result_get = float(result1[0][j])+(float(result2[0][j])-float(result1[0][j]))*rate
            # print(data.iloc[i,index])
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

# 厂内参数
def fact_data(i, data, result, index_list):

    date_fact = result[i][1]
    time_fact = result[i][2]

    date_lake = result[i][22]
    time_lake = result[i][23]

    date_before_str = date_lake.isoformat()[0:10] # 转换为字符串
    date_behind_str = date_fact.isoformat()[0:10] # 转换为字符串

    time_lake = str(time_lake)
    time_fact = str(time_fact)
    time_lake_hour = datetime.datetime.strptime(time_lake, '%H:%M:%S').hour
    time_fact_hour = datetime.datetime.strptime(time_fact, '%H:%M:%S').hour
    time_before_str = f'{time_lake_hour}:00:00'

    time_behind_str = time_fact
    print(date_before_str, date_behind_str)
    print(time_before_str, time_behind_str)
    if time_lake_hour > time_fact_hour:
        sql1 = f"SELECT * FROM baiyangwancorr WHERE 厂内日期='{date_before_str}' and '{time_before_str}'<=厂内时间"
        sql2 = f"SELECT * FROM baiyangwancorr WHERE 厂内日期='{date_behind_str}' and '{time_behind_str}'>=厂内时间"

        result1 = query_read(sql1)
        result2 = query_read(sql2)
        print(result1)
        print('++')
        print(result2)
        result1111 = result1+result2  # 合并元组
        print(result1111)
    else:
        sql = f"SELECT * FROM baiyangwancorr WHERE 厂内日期='{date_before_str}' and 厂内时间 between'{time_before_str}'and'{time_behind_str}'"
        result1111 = query_read(sql)

    if len(result1111) != 0 :  # 可以插值
        list = []
        print(len(result1111))
        print(result1111)
        for x in index_list:
            for j in range(len(result1111)):
                list.append(float(result1111[j][x]))
            # print(*list)
            mean = np.mean(np.array(list))
            print(data.iloc[i, x],'-->',mean)
            data.iloc[i, x] = mean
    return data

sql = f'select * from baiyangwancorr'
result = query_read(sql)
data = pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\baiyangwancorr.csv', index_col=None))
try:
    for index,i in enumerate(result):
        print(index,'---------------------')
        find_data(index, data, result, [3,4,5,6,7,8,9,10,19,20])
        find_data(index, data, result,[15])
        data = fact_data(index, data, result,[12,13,14])
finally:
    # 去掉时间一列有0值的行（非测量值经处理后为0）
    data = data.dropna(subset=[u'厂内时间'], inplace=False)  # 此处inplace不可改为True，否则输出None
    data.to_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\baiyangwancorr1.csv',index=False)