import codecs
import jieba
import jieba.analyse
import pickle
import numpy as np
from scipy.misc import imread
from wordcloud import WordCloud, ImageColorGenerator
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# 生产词云文本
def seg_sentence(file_name):
    file = open('dict_name.txt', 'rb')  # 读取dict_name文档，用于jieba的自定义词典和关键词的筛选
    dict_name = pickle.load(file)
    print(dict_name)
    jieba.load_userdict(dict_name)
    with codecs.open(file_name, encoding='utf-8') as f:  # 读取文档
        original_text = f.read()
    wordList = jieba.cut(original_text)  # 全文分词，结果存储在wordlist中
    print('---全文分词完成---')
    allow_pos = ('nr',)  # 设置筛选参数为”nr“,名字
    tags = jieba.analyse.extract_tags(original_text, topK=1000, withWeight=False,
                                      allowPOS=allow_pos)  # 从原文文本original_text中，筛选词性为”nr“的前30个词汇作为关键词
    print('---关键词筛选完成---')
    stags = " ".join(tags)  # 将关键词通过空格连接为字符串stags

    f2 = open(u"stags.txt", "w+")  # 将获得的关键词存储到stags.txt文件中（供调试查看）
    f2.write(stags)
    f2.write("\n")
    f2.close()

    count = 0
    outstr = ''
    for word in wordList:  # 遍历全文分词结果wordlist
        if word in stags:  # 与关键词字符串比较，只保留关键词
            if word in dict_name:  # 在关键词中只保留人名
                if len(word) > 1:  # 去掉长度小于1的词
                    if word != '\t':
                        outstr += word
                        outstr += " "
                        count = count + 1
    print("---词云文本完成---")
    print(outstr)
    return outstr  # 将保留下的词输出到字符串outstr中，通过空格连接为字符串


# 绘制词云
def draw_wordcloud(file_name):
    outstr = seg_sentence(file_name)  # 调用分词函数，生成只包含关键词的分词文本outstr,字符串格式
    f2 = open(u"分词后.txt", "w+")  # 将outstr保存到 分词后.txt文件中 （供调试查看）
    f2.write(outstr)
    f2.write("\n")
    f2.close()


    color_mask = imread("sanguo.jpg")  # 读取模板图片

    # 设置词云参数，字体，模板，背景白色，最大词量1000个，最大字体尺寸60
#    cloud = WordCloud(background_color='white', mask=color_mask, font_path='simhei.ttf')
    cloud = WordCloud(font_path='simhei.ttf', background_color='white', mask=color_mask, max_words=1000, min_font_size=1,
                      max_font_size=60, scale=2, height=500, width=500, relative_scaling=0.5)

    word_cloud = cloud.generate(outstr)  # 产生词云数据 word_cloud
    print("---词云完成---")
    word_cloud.to_file("w_cloud.jpg")  # 词云保存为图片w_cloud.jpg
    print("---词云保存成功---")
    return word_cloud


file_name = '三国演义替换文.txt'  # 设置小说文本所在路径

word_cloud = draw_wordcloud(file_name)  # 调用词云生成函数，生成词云word_cloud，并保存成为图片
plt.figure(figsize=(20, 20))
plt.imshow(word_cloud)
plt.axis("off")
plt.show()  # 显示词云图