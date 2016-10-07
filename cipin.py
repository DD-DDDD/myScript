import jieba#中文分词库
import codecs
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt


f = codecs.open("C:/Users/ricaito/Desktop/Knownsec_RD_Checklist_v3.0/zhidao.txt", "r", "utf-8")
content = f.read()
f.close()
def word_frequency(txt):
    words = [word for word in jieba.cut(txt,cut_all = True) if len(word) > 2 ]
    #jieba 分词
    counts = Counter(words)
    #统计次数
    for word_freq in counts.most_common(11):
        #统计次数出现频率最高的11个字
        word, freq = word_freq
        #word_freq 为列表(由元组组成的列表）
        print(word,freq)
    wordcloud = WordCloud(font_path='./simheittf/simhei.ttf',    background_color="black",   margin=5, width=1800, height=800)
    wordcloud = wordcloud.generate(str(counts.most_common(14)))
    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


word_frequency(content)












