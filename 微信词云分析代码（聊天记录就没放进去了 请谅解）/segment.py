# coding:utf-8
import jieba
import numpy
import codecs
import pandas
import matplotlib.pyplot as plt
from scipy.misc import imread
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from wordcloud import WordCloud
import re
import codecs
# 将聊天记录转变为纯汉字，除去微信结构中的符号
with codecs.open('聊天记录_cft.txt', 'r' ,encoding = 'utf-8') as file:
    f = file.read()
    k = re.findall(r'[\u4e00-\u9fa5]+', f)

data=open("聊天记录_cft_hanzi.txt",'w+',encoding='utf-8')
for i in k:
    data.write(i+'\n')
data.close()

def load_file_segment():
    # 读取文本文件并分词
    f = codecs.open(u"聊天记录_cft_hanzi.txt",'r',encoding='utf-8')
    # 打开文件
    content = f.read()
    # 读取文件到content中
    f.close()
    # 关闭文件
    segment=[]
    # 保存分词结果
    segs=jieba.cut(content)
    # 对整体进行分词
    for seg in segs:
        if len(seg) != 1 and seg != '\r\n':
            # 如果说分词得到的结果非单字，且不是换行符，则加入到数组中
            segment.append(seg)
    return segment

def get_words_count_dict():
    segment = load_file_segment()
    # 获得分词结果
    df = pandas.DataFrame({'segment':segment})
    # 将分词数组转化为pandas数据结构
    stopwords = pandas.read_csv("stopwords.txt",index_col=False,quoting=3,sep="\t",names=['stopword'],encoding="utf-8")
    # 加载停用词
    df = df[~df.segment.isin(stopwords.stopword)]
    # 如果不是在停用词中
    words_count = df.groupby('segment').agg(
        计数=pandas.NamedAgg(column='segment', aggfunc='size')).reset_index().sort_values(
        by='计数', ascending=False)

    # 按词分组，计算每个词的个数
    words_count = words_count.reset_index().sort_values(by="计数",ascending=False)
    # reset_index是为了保留segment字段，排序，数字大的在前面
    return words_count

words_count = get_words_count_dict()
# 获得词语和频数

bimg = imread('ai.jpg')
# 读取我们想要生成词云的模板图片
wordcloud = WordCloud(background_color='white', mask=bimg, font_path='simhei.ttf')
# 获得词云对象，设定词云背景颜色及其图片和字体

# 如果你的背景色是透明的，请用这两条语句替换上面两条
# bimg = imread('ai.png')
# wordcloud = WordCloud(background_color=None, mode='RGBA', mask=bimg, font_path='simhei.ttf')

words = words_count.set_index("segment").to_dict()
# 将词语和频率转为字典
wordcloud = wordcloud.fit_words(words["计数"])
# 将词语及频率映射到词云对象上
bimgColors = ImageColorGenerator(bimg)
# 生成颜色
plt.axis("off")
# 关闭坐标轴
plt.imshow(wordcloud.recolor(color_func=bimgColors))
# 绘色
plt.show()