import datetime
import math

import numpy as np
import jieba
import pandas as pd
from harvesttext import HarvestText
import matplotlib.pyplot as plt
import matplotlib.dates as mdate


#读取微博评论并添加列表
def txt_read(path):
    content_list=[]
    count=0
    with open(path,"r",encoding='utf-8')as txt_f:
        for line in txt_f.readlines():
            if count!=0:
                line=line.strip('\n')
                content_list.append(line)
            count+=1
    return content_list
#分词函数
def word_cut(doc,stpword):
    wordlist=result=[k for k in jieba.cut(doc,cut_all=False) if k not in stpword ]
    return wordlist

jieba.load_userdict("stopwords_list.txt")
jieba.load_userdict("disgust.txt")
jieba.load_userdict("fear.txt")
jieba.load_userdict("joy.txt")
jieba.load_userdict("sadness.txt")
jieba.load_userdict("anger.txt")
stopword=[line.strip() for line in open("stopwords_list.txt","r",encoding="utf-8").readlines()]
ht=HarvestText()
#信息处理
def get_info(doc_list):
    info_list=[]
    for content in doc_list:
        weibo_info=content.split("\t")
        wb_time = weibo_info[3].split()
        if len(wb_time)>=4:
            wb_loca=weibo_info[0]
            del  wb_time[4]
            wb_time=" ".join(wb_time)
            wb_txt=ht.clean_text(weibo_info[1])
            wb_cut=word_cut(wb_txt,stopword)
            wb={"wb_txt":wb_txt,"wb_time":wb_time,"wb_loca":wb_loca,"wb_cut":wb_cut}
            info_list.append(wb)
    return info_list
#向量化

def emo_count():
    anger=txt_read("anger.txt")
    disgust=txt_read("disgust.txt")
    fear=txt_read("fear.txt")
    joy=txt_read("joy.txt")
    sadness=txt_read("sadness.txt")
    def count_0(wordlist):
        vec = [0, 0, 0, 0, 0]
        for word in wordlist:
            if word in anger:
                vec[0]+=1
            if word in disgust:
                vec[1]+=1
            if word in fear:
                vec[2]+=1
            if word in joy:
                vec[3]+=1
            if word in sadness:
                vec[4]+=1
        if sum(vec)==0:
            return vec
        else:
            vect=[k/sum(vec) for k in vec]
            return vect
    return count_0

def judge_word(vect):
    emo=vect[0]
    for k in vect:
        if emo != k :
            return True
    return False

def time_tansform(str0):
    str_time=datetime.datetime.strptime(str0,'%a %b %d %H:%M:%S %Y')

    return str_time



def loc_tansform(str1):
    lis=list(str1)
    del lis[0]
    del lis[-1]
    str2="".join(lis)
    loc_list=str2.split(',')
    loc=[float(k)for k in loc_list]
    return loc

def plot_emo_time(df1,emo,fre):
    df2=df1[emo]
    plot_emo=df2.resample(fre).mean()
    plot_emo.plot(marker='*')
    plt.show()
    return plot_emo

def disntance(df):
    g_x=df["wb_x"].mean()
    g_y=df["wb_y"].mean()
    df["wb_dis"]=df[["wb_x","wb_y"]].apply(lambda x: math.sqrt((x["wb_x"] - g_x) ** 2 + (x["wb_y"] - g_y) ** 2), axis=1)
    return df

def dis_plot(df1,emo):
    emo.append("wb_dis")
    df=df1[emo]
    dis=[]
    dis_emo=[]
    for i in range(10):
        dplot=df[:][(df["wb_dis"]>=2.45+0.02*i)&(df["wb_dis"]<=2.455+0.02*(i+1))]
        dplot=dplot[emo[0]].mean()
        dis.append(2.45+i*0.02)
        dis_emo.append(dplot)
    plt.plot(dis,dis_emo,marker='*')
    plt.show()
    return

content=txt_read("weibo.txt")
wb_list=get_info(content)
f0=emo_count()
wb_emo_list=[]
for info in wb_list:
    info["wb_vec"]=f0(info["wb_cut"])
    info["wb_time"]=time_tansform(info["wb_time"])
    info["wb_loca"]=loc_tansform(info["wb_loca"])
    info["wb_x"]=info["wb_loca"][0]
    info["wb_y"]=info["wb_loca"][1]
    if(judge_word(info["wb_vec"])):
        info["wb_emo"]=True
        wb_emo_list.append(info)
    else:
        info["wb_emo"]=False
print(wb_emo_list)
#顺序是：anger disgust fear joy sadness
df= pd.DataFrame(wb_emo_list)
df=df.set_index(pd.to_datetime(df["wb_time"]))
df["anger"]=[k[0] for k in df["wb_vec"]]
df["disgust"]=[k[1] for k in df["wb_vec"]]
df["fear"]=[k[2] for k in df["wb_vec"]]
df["joy"]=[k[3] for k in df["wb_vec"]]
df["sadness"]=[k[4] for k in df["wb_vec"]]
df.drop(columns=['wb_emo'],inplace=True)
df=disntance(df)
print(df["wb_dis"].mean())

#测试画图
plot_emo_time(df,["anger"],'SM')
dis_plot(df,["fear"])
