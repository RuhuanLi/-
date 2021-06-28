import re
import pandas as pd
import pickle

with open('namelist.txt', 'r', encoding='utf-8') as f:
    result = f.read()
    f.close()

# 去掉多余的空格
result = re.sub(r'\s+', '', result)

print(result)

# 以括号切分数据 ，把姓名和字号整理为字典格式
a = result.split("）")
del a[len(a) - 1]
dict_ming_zi = pd.DataFrame(columns=['ming', 'zi'])
j = 0
for i in a:
    dict_ming_zi.loc[j, 'ming'] = str(i).split("（")[0]
    dict_ming_zi.loc[j, 'zi'] = str(i).split("（")[1]
    j += 1


# 替换原文中的字号，并保存替换文本
with open('sanguo.txt', 'r', encoding='utf-8') as f1:
    original_text = f1.read()
    f1.close()
for i in range(len(dict_ming_zi)):
    original_text = original_text.replace(dict_ming_zi.iloc[i, 1], dict_ming_zi.iloc[i, 0])
with open('三国演义替换文.txt', 'w', encoding='utf-8') as f2:
    f2.write(original_text)
    f2.close()

# 将姓名及词性以字典的形式保存（该文件用于之后的词云生成）
list_ming = []
list_ming = dict_ming_zi['ming']
print(list_ming)
name_dict = {}
for i in list_ming:
    name_dict[i] = 'nr'
with open('dict_name.txt', 'wb') as f3:
    pickle.dump(name_dict, f3,0)
    f3.close()