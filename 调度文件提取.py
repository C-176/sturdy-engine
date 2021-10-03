import os
import shutil

file_list = []
delet_list = []
path1 = r"C:\Users\1\Desktop\调度"
files1 = os.listdir(path1)

for i in files1:
    path2 = path1+'\\'+'%s' % i
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
    shutil.move(file,r'C:\Users\1\Desktop\调度')  # 移动文件到指定文件夹
print('文件移动完成！')

for file_dir in delet_list:
    shutil.rmtree(file_dir)  # 删除指定文件夹
print('文件夹删除完成！')