#!/usr/bin/python
import pandas

data0 = pandas.read_csv('chat_log.csv', usecols=[7,8])
# 读取我们上一步提取出来的csv文件，这里要改成你自己的文件名
# print(data0)
# 根据数据集中的标签提取指定列的数据（根据talker提取content）
data1 = data0.groupby(by='talker').apply(lambda x:['\n'.join(x['content'])])
print(data1)

cft = data1.at['wxid_nplp27nxnjta12']
# 输出为文本文档
data=open("聊天记录_cft.txt",'w+',encoding='utf-8')
for i in cft:
    data.write(i+'\n')
    # 每行聊天记录换行
data.close()