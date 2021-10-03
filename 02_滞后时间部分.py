import datetime
import pymysql
from dbutils.pooled_db import PooledDB
import numpy as np
import pandas as pd


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

# Z-score原则
def ZScore(i, data, data_orig, index, threshold=3):
    data_d = np.array(data)
    mean_d = np.mean(data_d)
    print(i,'均值：',mean_d)
    std_d = np.std(data_d)

    outliers = []
    for index_last, y in enumerate(data_d):
        z_score = (y - mean_d) / std_d
        if np.abs(z_score) > threshold  or y <= 0:
            outliers.append(y)
            data_orig.iloc[index_last,index] = str(mean_d)
    return outliers,data_orig,mean_d

# 测试部分
# sql = f'alter table test change 日期 日期 date(3)'
# sql = f'alter table test modify column 日期 date(0)'
# query_write(sql)

data_colu_test = ['水源地原水浊度', '水源地耗氧量', '水源地PH值', '水源地水温',
       '水源地氨氮量', '水源地溶解氧', '水源地藻密度', '水源地电导率', '进厂原水浊度', '1200进厂水量',
       '1400进厂水量', '2号沉淀池进水水量', '2号沉淀池出水浊度']
dict_delete = {}
# 数据简单清洗
def data_clean():
    number = 0
    while number < 1:  # 3为数据处理的次数
        data_orig = pd.DataFrame(pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\baiyangwancorr.csv', index_col=None))
        # print(data_orig.columns)
        for index, i in enumerate(data_colu_test):
            data_d = data_orig[i]
            index += 3

            # Z-score法则
            list, data_orig, mean = ZScore(i, data_d, data_orig, index)
            dict_delete[i] = mean  # 此处是为了后面提出异常数据。
        try:
            data_orig.to_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\baiyangwancorr.csv', index=False)
        finally:
            print(f'第{number + 1}次数据清洗完毕！')

        number += 1
        # for i in dict_delete.keys():
        #     print(f"'{i}':'{dict_delete[i]}'",end=',')

data_clean()


sql = 'alter table baiyangwancorr add (水源地日期 varchar(255),水源地时间 time(0))'
query_write(sql)
sql = 'alter table baiyangwancorr add (出水日期 varchar(255),出水时间 time(0))'
query_write(sql)
sql = 'select * from baiyangwancorr'
data = query_read(sql)  # 获得多元数据流
number = 1  # id初始值
for i in data:
    date1 = str(i[1])  # 日期
    time1 = str(i[2])  # 时间
    # if time1 == '24:00:00':
    #     time1 = '23:59:59'  # 由于%H范围是0-23，直接用24时的话，不行。
    water1 = float(i[12]) + float(i[13])  # 总进厂水量
    water2 = float(i[14])  # 二号池进水量
    time_cha1 = 14500 / (water1 / 2.669)  # 根据公式计算滞后时间1（从水源地到水厂之间的时间），单位是（小时）
    if water2 != 0:
        time_cha2 = (3125 / water2) * 2  # 根据公式计算滞后时间2（从水进入厂到出沉淀池所耗时间近似看为沉淀池反应时间），单位是（小时）
    else:
        time_cha2 = 0
        print("被除数为0，迫不得已")

    now_time = date1 + ' ' + time1  # 将日期时间合并成str
    now_time_datetime = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')  # 转为datetime格式以便计算
    lake_time = now_time_datetime + datetime.timedelta(hours=-time_cha1)  # 计算对应的水源地时刻
    pool_time = now_time_datetime + datetime.timedelta(hours=+time_cha2)
    print('厂内时间:', now_time)
    print('进厂总水量:%s立方米 ' % water1, ' 滞后时间1 :%f时' % time_cha1, ' 滞后时间2 :%f时' % time_cha2)

    lake_time_str = lake_time.isoformat()  # 转为字符串
    lake_date_last = lake_time_str[:10]
    lake_time_last = lake_time_str[11:19]
    print('水源地时间:', lake_date_last, lake_time_last)
    pool_time_str = pool_time.isoformat()
    pool_date_last = pool_time_str[:10]
    pool_time_last = pool_time_str[11:19]
    print('沉淀池出水时间:', pool_date_last, pool_time_last)


    # sql = "update baiyangwan set %s='01:02:02' where id=2" % ('出水时间')
    # sql = 'insert into baiyangwan(%s) values("%s")' % ('出水时间','01:01:01')
    sql = "update baiyangwancorr set 出水时间='%s',出水日期='%s',水源地时间='%s',水源地日期='%s' where id = %d" \
          % (pool_time_last, pool_date_last, lake_time_last, lake_date_last, number)
    query_write(sql)
    number += 1
    print(number,'*'*20)
print(dict_delete)
# 想更改数据库某些字条的类型
# sql = f'alter table baiyangwancorr change 厂内日期 厂内日期 varchar(10)'
# query_write(sql)


