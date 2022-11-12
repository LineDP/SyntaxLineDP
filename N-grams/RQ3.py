#!/usr/bin/env python3
# coding=utf-8

import copy
from doctest import testfile
import urllib
import re
import random
import string
import operator
import numpy as np
import pandas as pd
from sklearn.metrics import recall_score,precision_score,f1_score
from init import *

'''
实现了 NGram 算法，并对 markov 生成的句子进行打分；
'''
class ScoreInfo:
    score = 0
    content = ''

class NGram:
    __dicWordFrequency = dict() #词频
    __dicPhraseFrequency = dict() #词段频
    __dicPhraseProbability = dict() #词段概率

    def printNGram(self):
        print('词频')
        for key in self.__dicWordFrequency.keys():
            print('%s\t%s'%(key,self.__dicWordFrequency[key]))
        print('词段频')
        for key in self.__dicPhraseFrequency.keys():
            print('%s\t%s'%(key,self.__dicPhraseFrequency[key]))
        print('词段概率')
        for key in self.__dicPhraseProbability.keys():
            print('%s\t%s'%(key,self.__dicPhraseProbability[key]))

    def append(self,content):
        '''
        训练 ngram  模型
        :param content: 训练内容
        :return: 
        '''
        #clear
        # content = re.sub('\s|\n|\t','',content)
        content=content[1:-1].replace(" ","").replace("\'","").split(",")
        ie = self.getIterator(content) #2-Gram 模型
        keys = []
        for w in ie:
            #词频
            k1 = w[0]
            k2 = w[1]
            if k1 not in self.__dicWordFrequency.keys():
                self.__dicWordFrequency[k1] = 0
            if k2 not in self.__dicWordFrequency.keys():
                self.__dicWordFrequency[k2] = 0
            self.__dicWordFrequency[k1] += 1
            self.__dicWordFrequency[k2] += 1
            #词段频
            key = '%s %s'%(w[0],w[1])
            keys.append(key)
            if key not in self.__dicPhraseFrequency.keys():
                self.__dicPhraseFrequency[key] = 0
            self.__dicPhraseFrequency[key] += 1

        #词段概率
        for w1w2 in keys:
            w1 = w1w2.split(" ")[0]
            # print(w1)
            w1Freq = self.__dicWordFrequency[w1]
            w1w2Freq = self.__dicPhraseFrequency[w1w2]
            # P(w1w2|w1) = w1w2出现的总次数/w1出现的总次数 = 827/2533 ≈0.33 , 即 w2 在 w1 后面的概率
            self.__dicPhraseProbability[w1w2] = round(w1w2Freq/w1Freq,2)
        pass

    def getIterator(self,txt):
        '''
        bigram 模型迭代器
        :param txt: 一段话或一个句子
        :return: 返回迭代器，item 为 tuple，每项 2 个值
        '''
        ct = len(txt)
        if ct<2:
            return txt
        for i in range(ct-1):
            w1 = txt[i]
            w2 = txt[i+1]
            yield (w1,w2)

    def getScore(self,txt):
        '''
        使用 ugram 模型计算 str 得分
        :param txt: 
        :return: 
        '''
        ie = self.getIterator(txt)
        score = 1
        fs = []
        for w in ie:
            key = '%s %s'%(w[0],w[1])
            freq = self.__dicPhraseProbability[key] if key in self.__dicPhraseProbability.keys() else 0.01
            fs.append(freq)
            score = freq * score
        #print(fs)
        #return str(round(score,2))
        # info = ScoreInfo()
        # info.score = score
        # info.content = txt
        return score

    def sort(self,infos):
        '''
        对结果排序
        :param infos: 
        :return: 
        '''
        return sorted(infos,key=lambda x:x.score,reverse=True)


def fileReader(project):
    path = "./wp_traindata/"
    with open(path+project,'r',encoding='utf-8') as f:
        rows = 0
        # 按行统计
        while True:
            rows += 1
            line = f.readline()
            if not line:
                print('读取结束 %s'%path)
                return
            # print('content rows=%s len=%s type=%s'%(rows,len(line),type(line)))
            yield line
    pass


def myreplace(matched):
    return " " + matched.group(0) + " "


def get_test(project):
    test_files=[]
    test_project=copy.deepcopy(projects)
    test_project.remove(project)
    print(test_project)
    for item in test_project:
        test_files.extend(all_releases[project][2:])
    df=[pd.read_csv(data_path+testfile+".csv") for testfile in test_files]
    df=pd.concat(df)
    return df

def main():
    ng = NGram()
    # project='activemq'
    recall_20_LOCs=[]
    effort_20_recalls=[]
    IFAs=[]
    for project in projects:
        reader = fileReader(project)
        #将语料追加到 bigram 模型中
        for row in reader:
            # print(row)
            ng.append(row)
        #ng.printNGram()
        #测试生成的句子，是否合理
        test_df=get_test(project)
        scores=[]
        for codeline in list(test_df['codelines']):
            #对生成的句子打分
            codeline=str(codeline)
            codeline = codeline.replace("\n", "").replace("\t", " ").replace("\/?", "").replace("\\", "")
            codeline = re.sub(r"[\W]", myreplace, codeline)
            codeline=codeline.split()
            score = ng.getScore(codeline)
            # print(score)
            scores.append(score)
        #排序
        test_df['score']=scores
        
        test_df=test_df.sort_values(by='score',ascending=True)
        line_label=list(test_df["line_label"])
        line_pred=list(test_df["score"])
        
        #计算recall@20%LOC
        predict=[1 for _ in range(int(len(line_label)*0.2))]
        length=len(predict)
        for _ in range(len(line_label)-length):
            predict.append(0)
        
        recall_20_LOC=recall_score(line_label,predict)
        recall_20_LOCs.append(recall_20_LOC)
        
        #计算effort@20%Recall
        total_defect=line_label.count(1)
        top20_defect=int(total_defect*0.2)
        TP=0
        count=0
        for i in range(len(line_label)):
            if line_label[i] :
                TP+=1
                if TP==top20_defect:
                    count=i
        effort_20_recall=float(count/len(line_label))
        effort_20_recalls.append(effort_20_recall)
        
        #计算IFA
        #计算IFA，计算范围是有缺陷的文件
        IFA=[]
        test_df = test_df.drop(index=test_df[test_df['file_label'] == False].index).reset_index().drop('index', axis=1)
        for file,df_ in test_df.groupby("filename"):
            df_=df_.sort_values(by='score',ascending=True)
            labels=list(df_['line_label'])
            for index,label in enumerate(labels):
                if label==1:
                    IFA.append(index+1)
                    break
        IFAs.append(np.mean(IFA))

        with open("cp_result.txt",'a') as f:
            f.write(project+" recall_20_LOC: "+str(recall_20_LOC)+" effort@20%Recall: "+str(effort_20_recall)+"\n")
    dic={"projects":projects,"recall@20%LOC":recall_20_LOCs,"effort@20%Recall":effort_20_recalls,"IFA":IFAs}
    df=pd.DataFrame(dic)
    df.to_csv("cp_result.csv",index=False)


if __name__ == '__main__':
    main()
    pass