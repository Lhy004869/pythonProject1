
import collections
import csv
import math
import matplotlib.pyplot as plt
import numpy as np


def word_freq(wordlist):
    freq_wordtopn=items[0:50]
    return freq_wordtopn
#1.
print("读入弹幕")
with open("danmuku.csv",'r',encoding='utf-8') as csv_file:
    csv_reader=csv.reader(csv_file)
    lis=[]
    a=0
    for row in csv_reader:
        if a!=0:
            lis.append(row[0])
        a+=1
words="".join(lis)

import jieba
jieba.load_userdict("stopwords_list.txt")
stopword=[line.strip() for line in open("stopwords_list.txt","r",encoding="utf-8").readlines()]
stopword.append(" ")
result=[k for k in jieba.cut(words,cut_all=False) if k not in stopword ]

#2.
counts={}
for word in result:
    counts[word] = counts.get(word,0)+1
items = list(counts.items())
items.sort(key=lambda x:x[1], reverse=True)
print("词频统计为：",items)
print()
#3.
print("特征集筛选")
special_Solicitation= word_freq(items)
print("高频集为：",special_Solicitation)
print()
special_Solicitation0=[]
for word in special_Solicitation:
    special_Solicitation0.append(word[0]);
print("特征词组为：",special_Solicitation0)
#4.
print("进行向量化弹幕")
with open("danmuku.csv",'r',encoding='utf-8') as csv_file:
    csv_reader=csv.reader(csv_file)
    vector=[]
    a=0
    for row in csv_reader:
        if a!=0:
            vec=[0]*len(special_Solicitation0)
            for word in special_Solicitation0:
                if word in row[0]:
                    vec[special_Solicitation0.index(word)]=1
            vector.append(vec)
        a+=1

#5.
print("测试")
dis_list=[0]*len(vector)
gravity=[0]*len(special_Solicitation0)#重心
for x in range(0,len(vector)):
    for y in range(0,len(vector[0])):
        gravity[y]+=vector[x][y]
gravity=[k/len(vector) for k in gravity]
print(gravity)
for x in range(0,len(vector)):#距离
    for y in range(0,len(vector[0])):
        dis_list[x]+=(vector[x][y]-gravity[y])**2
dis_list=[math.sqrt(k) for k in dis_list]
word_max=dis_list.index(max(dis_list))
word_min=dis_list.index(min(dis_list))

print("差距最大的两组弹幕")
with open("danmuku.csv",'r',encoding='utf-8') as csv_file:
    csv_reader=csv.reader(csv_file)
    a=-1
    for row in csv_reader:
        if a==word_max or a==word_min:
            print(row[0])
        a+=1

#6.
print("词云统计")
import wordcloud
top50word=items[0:50]
word_dict=dict(top50word)
wc = wordcloud.WordCloud(font_path="msyh.ttc",width = 1000,height = 700,background_color = "white")
wc.generate_from_frequencies(word_dict)
plt.imshow(wc)
plt.axis('off')
plt.show()

