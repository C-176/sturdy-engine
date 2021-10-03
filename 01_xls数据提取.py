import datetime
import time
import os
import numpy as np
import pandas
import pandas as pd
import shutil
import xlrd
from xlrd.xldate import xldate_as_datetime

# 实现完全保存新数据
shutil.rmtree(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv')  # 删除指定文件夹
os.mkdir(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv')  # 新建文件夹


# 调度文件移动
def diaoduFileMove():
    file_list = []
    delet_list = []
    path1 = r"C:\Users\1\Desktop\调度"
    files1 = os.listdir(path1)

    for i in files1:
        path2 = path1 + '\\' + '%s' % i
        delet_list.append(path2)
        files2 = os.listdir(path2)
        for j in files2:
            path3 = path2 + '\\' + '%s' % j
            files3 = os.listdir(path3)
            for f in files3:
                file = path3 + '\\' + '%s' % f
                if list(file)[-4] == '.':
                    file_list.append(file)

    for file in file_list:
        shutil.move(file, r'C:\Users\1\Desktop\调度19-21')  # 移动文件到指定文件夹
    print('文件移动完成！')

    for file_dir in delet_list:
        shutil.rmtree(file_dir)  # 删除指定文件夹
    print('文件夹删除完成！')


# 藻密度专用补0：根据列表线性插值
def linear_cha_zao(i, list):
    value1 = 0
    for ind, num in enumerate(list[i - 4:i - 1]):
        if num != '':
            value1 = float(num)
            break
    value2 = 0
    ind = 1
    for ind, num in enumerate(list[i + 1:i + 100]):
        if num != '':
            value2 = num
            ind = 3 - ind
            break
    if value1 > value2:
        list[i] = value1 - (value1 - value2) * (ind / 4)
    else:
        list[i] = value1 + (value2 - value1) * (ind / 4)
    return list[i]


# 普通补0，前后值取平均
def linear_cha_normal(i, list):
    value1 = list[i - 1]  # 直接取前一个值
    value2 = 1
    for num in list[i + 1:i + 100]:
        if num != 0:
            value2 = num
            print('线性插值成功!')
            break
    value = (value1 + value2) / 2
    return value


# 读取文件夹下全部文件名，存入list
def get_files_list(path):
    files = os.listdir(path)

    path_list = []
    date_list = []
    for i in files:
        path1 = path + '\\' + i
        path_list.append(path1)
        date_list.append(i[0:-4])
    return path_list, date_list


# 转换成csv文件并进行写入磁盘
def Tocsv(index, name):
    # col_num = workbook.ncols
    list = []
    if name == '厂内时间':
        rows = workbook.nrows
        for i in range(rows):
            value1 = workbook.cell(i, index).value
            value3 = None
            if type(value1) == float:
                value2 = xldate_as_datetime(value1, 0)
                value3 = value2.strftime('%H:%M:%S')
            list.append(value3)
        list = list[6:32]

    else:
        if name in special_list:
            list = workbook.col_values(index)[5:31]
        elif name in special_list2:
            list = workbook.col_values(index)[7:33]
        else:
            list = workbook.col_values(index)[6:32]
        # 看看有没有缺值，若有，调用插值函数插
        for i in range(len(list)):  # 为什么不在取数据的时候就插值，是因为想把数据取完之后根据前后文做插值，要不然有可能一个文件中这个数据全部为0 ，那如何插值呢？
            value = list[i]
            if name == '水源地藻密度':
                if value == '' or value == 0:
                    # print('开始线性插值！')
                    list[i] = linear_cha_zao(i, list)
            if name in list0:
                # 针对有必要进行补0动作的参数，调用函数进行补零
                if value == 0:
                    # print('开始插值！')
                    list[i] = linear_cha_normal(i, list)

        if '' in list:
            print('有None在列表中', name)

    # 生成DataFrame文件供写入csv
    csv_ = pandas.DataFrame(list, columns=[name])
    filepath = r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\%s.csv' % name
    # 判断文件是否存在，存在则追加，否则直接新建文件
    if os.path.exists(filepath):
        # print('文件存在了')
        csv_.to_csv(filepath, index=False, header=False, mode='a+')
    else:
        csv_.to_csv(filepath, index=False)
        file_list.append(filepath)

    return file_list


start_time = time.time()
# diaoduFileMove()  # 调度文件提取到一个文件夹中，只用一次就行了
path1_list, date1_list = get_files_list(path=r"C:\Users\1\Desktop\19-21")
path2_list, date2_list = get_files_list(path=r"C:\Users\1\Desktop\调度19-21")
file_list = []  # 文件列表，用以最后合并DataFrame

date_file = r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\厂内日期.csv'

for index, (path1, path2) in enumerate(zip(path1_list, path2_list)):
    # 首先处理日期一列
    list1 = []
    for i in range(6, 32):  # （6，32）以及后面的（5，31）都是根据xls表格的结构确定的。
        list1.append(date1_list[index])
    date_csv = pandas.DataFrame(list1, columns=['厂内日期'])
    if os.path.exists(date_file):
        date_csv.to_csv(date_file, index=False, header=False, mode='a+')
    else:
        date_csv.to_csv(date_file, index=False)

    # excel文件操作
    """print(book.sheet_names())  # 文件中的所有表
    data1 = book.sheet_by_index(0)   # 根据表的索引打开表
    workbook = book.sheet_by_name('常规工艺')  # 根据表名打开表
    print(workbook.name,workbook.nrows,workbook.ncols)  # 表名，表行数，表列数
    print(workbook.row_values(1))  # 读取行数据
    print(workbook.col_values(1))  # 读取列数据
    print(workbook.row_slice(6))  # 读取指定行数据类型"""

    special_list = ['水源地1#泵流量', '水源地1#加氯点投加量', '水源地2#泵流量', '水源地2#加氯点投加量', '进厂臭氧预投加量', '进厂臭氧气体流量']
    special_list2 = ['水源地藻密度', '水源地溶解氧']
    list0 = ['1200进厂水量', '1400进厂水量', '2号沉淀池进水水量']
    # 以上三个列表对应的数据在xls文件中的位置不一样，故，分情况存储。

    file = path1
    book = xlrd.open_workbook(file)  # 打开文件
    workbook = book.sheet_by_name('常规工艺')  # 根据表名打开表
    Tocsv(2, '厂内时间')
    Tocsv(3, '水源地原水浊度')
    Tocsv(4, '水源地耗氧量')
    Tocsv(5, '水源地PH值')
    Tocsv(6, '水源地水温')
    Tocsv(7, '水源地氨氮量')
    # Tocsv(8, '水源地溶解氧')

    # file = path2
    # book = xlrd.open_workbook(file)  # 打开文件
    # workbook = book.sheet_by_name('常规工艺')  # 根据表名打开表
    # Tocsv(11, '水源地溶解氧')  # 用调度文件中的溶解氧

    file = path1
    book = xlrd.open_workbook(file)  # 打开文件
    workbook = book.sheet_by_name('常规工艺')  # 根据表名打开表
    Tocsv(9, '水源地电导率')
    Tocsv(10, '进厂原水浊度')
    Tocsv(12, '1200进厂水量')
    Tocsv(14, '1400进厂水量')
    Tocsv(23, '2号沉淀池进水水量')
    Tocsv(29, '2号沉淀池出水浊度')

    workbook = book.sheet_by_name('加药')  # 根据表名打开表
    Tocsv(30, '2号矾投加量')
    workbook = book.sheet_by_name('次氯酸钠')  # 根据表名打开表
    Tocsv(19, '进厂1#加氯点投加量')
    Tocsv(22, '进厂1-1泵流量')
    Tocsv(23, '进厂1-2泵流量')
    Tocsv(24, '进厂2#加氯点投加量')
    Tocsv(27, '进厂2-1泵流量')
    Tocsv(28, '进厂2-2泵流量')
    workbook = book.sheet_by_name('金墅次氯酸钠')  # 根据表名打开表
    Tocsv(7, '水源地1#加氯点投加量')
    Tocsv(8, '水源地1#泵流量')
    Tocsv(10, '水源地2#加氯点投加量')
    Tocsv(11, '水源地2#泵流量')
    workbook = book.sheet_by_name('臭氧发生')  # 根据表名打开表
    Tocsv(11, '进厂臭氧气体流量')
    file_list = Tocsv(14, '进厂臭氧预投加量')

    file = path2
    book = xlrd.open_workbook(file)  # 打开文件
    workbook = book.sheet_by_name('常规工艺')  # 根据表名打开表
    Tocsv(11, '水源地溶解氧')
    file_list = Tocsv(12, '水源地藻密度')

    print('%s和%s写入完毕！' % (path1_list[index], path2_list[index]))

    # 将时间戳转化成格式显示
    """
    cellValue1 = workbook.cell(10,2).value
    cellValue2=xldate_as_datetime(cellValue1,0) 此处的0是指以1900为基准。
    cellValue3=cellValue2.strftime('%H:%M:%S')
    print("时间：",cellValue3)"""

# 全部文件夹遍历完毕之后再合并!!!
file_list.insert(0, date_file)
file_list.remove(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\水源地溶解氧.csv')
file_list.insert(7, r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\水源地溶解氧.csv')
file_list.remove(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\水源地藻密度.csv')
file_list.insert(8, r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\水源地藻密度.csv')

# 将多个单列csv文件存于list中
creat1 = locals()
csv_list = []
print('共%d列数据' % len(file_list))
for index, csvfile in enumerate(file_list):  # 此处涉及到生成同结构变量诸如 csv1\csv2.......\csvn的方法，不过没有必要。
    # print('合并第%d个' % index)
    # creat1['csv' + str(index)] = pd.read_csv(csvfile))
    # creat1['csv' + str(index)])
    # print('合并第%d个完成' % index)
    csv_list.append(pd.read_csv(csvfile))

# 合并多个单列csv
frames = [*csv_list]
all_csv = pd.concat(frames, axis=1)

# 条件判断！
all_csv.loc[all_csv[all_csv['进厂1-1泵流量'] == 0.0][all_csv['进厂1-2泵流量'] == 0.0].index, '进厂1#加氯点投加量'] = 0.0
all_csv.loc[all_csv[all_csv['进厂2-1泵流量'] == 0.0][all_csv['进厂2-2泵流量'] == 0.0].index, '进厂2#加氯点投加量'] = 0.0
all_csv.loc[all_csv['水源地1#泵流量'] == 0, '水源地1#加氯点投加量'] = 0
all_csv.loc[all_csv['水源地2#泵流量'] == 0, '水源地2#加氯点投加量'] = 0
all_csv.loc[all_csv['进厂臭氧气体流量'] == 0, '进厂臭氧预投加量'] = 0
# print(all_csv)
delete_list = ['进厂1-1泵流量', '进厂1-2泵流量', '进厂2-1泵流量', '进厂2-2泵流量', '水源地1#泵流量', '水源地2#泵流量', '进厂臭氧气体流量']
all_csv = all_csv.drop(columns=delete_list, axis=1)
# print(all_csv)

try:
    # 去掉时间一列有0值的行（非测量值经处理后为0）
    all_csv = all_csv.dropna(subset=[u'厂内时间'], inplace=False)  # 此处inplace不可改为True，否则输出None
    for i in range(len(all_csv)):
        if all_csv.iloc[i,1] == '00:00:00':
            dt = datetime.datetime.strptime(all_csv.iloc[i, 0],'%Y-%m-%d')+datetime.timedelta(days=1)
            all_csv.iloc[i, 0] = dt.isoformat()[0:10]
finally:
    print(all_csv)
    all_csv.index = range(1, len(all_csv) + 1)  # 把index转化为从1开始索引
    all_csv.to_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\baiyangwan.csv', index_label='id')

shutil.copyfile(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\baiyangwan.csv',
                r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv\baiyangwancorr.csv')

end_time = time.time()
use_time = datetime.timedelta(seconds=(end_time - start_time) // 1)
print('总用时:', use_time)  # 打印用时
print('任务完成，请查看！')
