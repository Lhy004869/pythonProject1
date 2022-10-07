import jieba
import matplotlib.pyplot as plt
import numpy as np
from harvesttext import HarvestText
import re

class Tokenizer:
    def __init__(self, chars, coding='c', PAD=0):
        dic = {}
        dic['PAD'] = PAD
        str0=' '.join(chars)
        self.coding = coding
        self.pad = PAD
        k = 1
        if coding == 'c':
            for char in str0:
                if char not in dic.keys():
                    dic[char]=k
                    k+=1
        elif coding == 'w':
            for char in jieba.lcut(str0):
                if char not in dic.keys():
                    dic[char]=k
                    k+=1
        self.lis = chars
        self.chars = dic

    def tokenize(self,sentence):
        if self.coding == 'c':
            return list(sentence)
        elif self.coding == 'w':
            return jieba.lcut(sentence)

    def encode(self,list_of_chars):
        num=[]
        for i in list_of_chars:
            num.append(self.chars[i])
        return num

    def trim(self,tokens,seq_len):
        if len(tokens)<seq_len:
            for i in range(seq_len-len(tokens)):
                tokens.append(0)
        elif len(tokens)>seq_len:
            tokens=tokens[0:seq_len]
        return tokens

    def decode(self,tokens):
        dic=dict((v,k) for k,v in self.chars.items())
        for i in range(len(tokens)):
            if tokens[i] == 0:
                if i == len(tokens) - 1:
                    print("[PAD]")
                else:
                    print("[PAD]",end='')
            else:
                if i == len(tokens) - 1:
                    print(dic[tokens[i]])
                else:
                    print(dic[tokens[i]],end='')
        return

    def encode_all(self,seq_len):
        num_lis=[]
        for i in self.lis:
            tok = Tokenizer.tokenize(self,i)
            num = Tokenizer.encode(self,tok)
            if len(num) == seq_len:
                num_lis.append(num)
        return  num_lis

def cleanword():
    with open('final_none_duplicate.txt','r',encoding='utf-8') as f:
        txt = f.readlines()
        lis=[]
        for text in txt:
            text_list=text.split("\t")
            text=text_list[1]
            #print(text)
            if '分享图片' in text:
                continue
            text = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:| |$)", " ", text)  # 去除正文中的@和回复/转发中的用户名
            text = re.sub(r"\[\S+\]", "", text)      # 去除表情符号
            # text = re.sub(r"#\S+#", "", text)      # 保留话题内容
            URL_REGEX = re.compile(
                r'(?i)\b((?:https?:\\/\\/|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
                re.IGNORECASE)
            text = re.sub(URL_REGEX, "", text)       # 去除网址
            text = text.replace("我在:", "")       # 去除无意义的词语
            text = text.replace("我在这里:","")
            text = re.sub(r"\s+", " ", text) # 合并正文中过多的空格
            text=text.rstrip()
            file = open('cleanword.txt','a',encoding='utf-8')
            file.write(text+'\n')

lis=[]
with open('cleanword.txt','r',encoding='utf-8') as f:
    for text in f.readlines():
      text=text.strip('\n')
      lis.append(text)
num_lis=[]
len_lis=[]
text=Tokenizer(lis,coding='w',PAD=0)
t=text.tokenize(text.lis[0])
tx=text.encode(t)
print(t)
print(tx)
txt=text.trim(tx,20)
txtt=text.decode(txt)
print(txtt)
print(txt)
#for i in text.lis:
    #t=text.tokenize(i)
    #num_lis.append(text.encode(t))
    #len_lis.append(len(text.encode(t)))
#n=np.median(len_lis)
#count_len_lis=[0 for k in range(max(len_lis)+1)]
#for l in len_lis:
    #count_len_lis[l]+=1
#plt.plot(range(len(count_len_lis)),count_len_lis,"-")
#plt.show()
#txt_list=text.encode_all(n)
#print(txt_list)