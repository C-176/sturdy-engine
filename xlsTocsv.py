import pandas
import pandas as pd
import shutil
import xlrd
from xlrd.xldate import xldate_as_datetime
import os

# shutil.move('06_深度学习/RF/日期.csv',r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\csv')

#TODO:数据清洗、全部提取

# 读取文件夹下全部文件名，存入list
path = r"C:\Users\1\Desktop\批量2016-2020"
files = os.listdir(path)
path_list = []
date_list = []
for i in files:
    path1 = path+'\\'+i
    path_list.append(path1)
    date_list.append(i[0:-4])

# print(*date_list)

file_list = []
date_file = u'日期.csv'
for index,path in enumerate(path_list):
    # 首先处理时间一列
    list1 = []
    for i in range(6, 34):
        list1.append(date_list[index])
    date_csv = pandas.DataFrame(list1, columns=['日期'])
    if os.path.exists(date_file):
        date_csv.to_csv(date_file, index=False, header=False, mode='a+')
    else:
        date_csv.to_csv(date_file, index=False)


    file = path
    book = xlrd.open_workbook(file)  # 打开文件


    # excel文件操作
    """print(book.sheet_names())  # 文件中的所有表
    data1 = book.sheet_by_index(0)   # 根据表的索引打开表
    print(workbook.name,workbook.nrows,workbook.ncols)  # 表名，表行数，表列数
    print(workbook.row_values(1))  # 读取行数据
    print(workbook.col_values(1))  # 读取列数据
    print(workbook.row_slice(6))  # 读取指定行数据类型"""

    # 追加csv
    # """
    # import pandas as pd
    # def write_csv(file,data):
    #     with open(file,'a') as f:
    #         csv_write = csv.writer(f)
    #         csv_write.writerows(data)
    #
    # file = pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\时间.csv')
    # data = pd.read_csv(r'C:\Users\1\Desktop\Python源码\06_深度学习\RF\水温.csv')
    # write_csv(file,data)  #data不行，得是str"""


    # 转换成csv文件并进行写入磁盘
    def Tocsv(index, name):

        # col_num = workbook.ncols
        if name == '时间':
            list = []
            rows = workbook.nrows
            for i in range(rows):
                value1 = workbook.cell(i,index).value
                value3 = 0
                if type(value1) == float :
                    value1 = workbook.cell(i, index).value
                    value2 = xldate_as_datetime(value1, 0)
                    value3 = value2.strftime('%H:%M:%S')
                list.append(value3)
            list = list[6:34]
        else:
            list = workbook.col_values(index)[6:34]
        # 生成DataFrame文件供写入csv
        csv_ = pandas.DataFrame(list,columns=[name])
        filepath =u'%s.csv' % name
        # 判断文件是否存在，存在则追加，否则直接新建文件
        if os.path.exists(filepath):
            # print('文件存在了')
            # 追加
            # csv1 = pandas.read_csv(filepath)
            # os.remove(filepath)
            # frame = [csv1,csv_]
            # csv0 = pandas.concat(frame,axis=1)

            csv_.to_csv(filepath,index=False,header = False, mode = 'a+')
            # print('追加完毕了')
        else:
            csv_.to_csv(filepath,index=False)
            file_list.append(filepath)
        # print('写入成功!')

        return file_list


    workbook = book.sheet_by_name('常规工艺')  # 根据表名打开表
    Tocsv(2, '时间')
    Tocsv(3, '原水浊度')
    Tocsv(4, '耗氧量')
    Tocsv(5, 'PH值')
    Tocsv(6, '水温')
    Tocsv(7, '氨氮量')
    Tocsv(8, '溶解氧')
    Tocsv(9, '进厂浊度')
    Tocsv(11, 'water1200')
    Tocsv(13, 'water1400')
    Tocsv(15, '回用水量')
    Tocsv(16, '配水井水位')
    Tocsv(22, '2号沉淀池进水水量')
    Tocsv(28, '2号沉淀池出水浊度')
    Tocsv(32, '砂滤池出水浊度')
    workbook = book.sheet_by_name('加药加氯加PAM')  # 根据表名打开表
    Tocsv(33,'2号冲程')
    Tocsv(34,'2号频率')
    Tocsv(44,'2号流量')
    Tocsv(45,'2号矾量')
    file_list = Tocsv(46,'2号投加量')


    print('%s写入完毕！'% path_list[index])

    # 将时间浮点数转化成正常的样子
    """
    cellValue1 = workbook.cell(10,2).value
    cellValue2=xldate_as_datetime(cellValue1,0)
    cellValue3=cellValue2.strftime('%H:%M:%S')
    print("时间：",cellValue3)"""


    # def show(list):
    #     for i in list:
    #         print(i)

    # data_csv = pd.DataFrame()
    # for index,i in enumerate(file_list):
    #     d1 = pd.read_csv(i)

    # df1 = pd.read_csv('time.csv')
    # df2 = pd.read_csv('zdjs.csv')


# 全部文件夹遍历完毕之后再合并!!!
creat1 = locals()
csv_list = []
# print('开始合并')
file_list.insert(0,date_file)
print('共%d列数据'% len(file_list))
for index,csvfile in enumerate(file_list):
    # print('合并第%d个' % index)
    creat1['csv'+str(index)] = pandas.read_csv(csvfile)
    csv_list.append(creat1['csv'+str(index)])
    # print('合并第%d个完成' % index)


frames = [*csv_list]
all_csv = pd.concat(frames,axis=1)
all_csv.to_csv('baiyangwan.csv',index=False)
print('任务完成，请查看！')





