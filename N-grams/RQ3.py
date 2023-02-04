import os
import numpy as np
import pandas as pd
import copy
from collections import Counter
from sklearn import preprocessing
from sklearn.metrics import recall_score,precision_score,f1_score, roc_auc_score,matthews_corrcoef
from init import *
import re

result_path="./cp_result/"
train_path="./wp_traindata/"
n=3


def probability(ngrams_counter,prefix_counter,sentence):
    prob = 1  # 初始化句子概率
    ngrams = list(zip(*[sentence[i:] for i in range(n)]))   # 将句子处理成n-gram的列表
    for ngram in ngrams:
        # 累乘每个n-gram的概率，并使用加一法进行数据平滑
        prob *= (1 + ngrams_counter[ngram]) / (len(prefix_counter) + prefix_counter[(ngram[0], ngram[1])])
    return prob

def get_test(project):
    test_files=[]
    test_project=copy.deepcopy(projects)
    test_project.remove(project)
    print(test_project)
    for item in test_project:
        test_files.extend(all_releases[item][2:])
        
    df_list=[]
    for testfile in test_files:
        df=pd.read_csv(data_path+testfile+".csv")
        filename=list(df['filename'])
        new_filename=[testfile+item for item in filename]
        df['filename']=new_filename
        df_list.append(copy.deepcopy(df))
    
    df=pd.concat(df_list)
    return df

aucs=[]
recalls=[]
precisions=[]
f1s=[]
balance_accs=[]
mccs=[]
recall_20_LOCs=[]
effort_20_recalls=[]
IFAs=[]

for project in projects:
    ngrams_list=[]
    prefix_list=[]
    with open(train_path+project) as f:
        for line in f:
            line=line[1:-1].replace(" ","").replace("\'","").split(",")
            ngrams=list(zip(*[line[i:] for i in range(n)]))
            prefix=list(zip(*[line[i:] for i in range(n-1)]))
            
            ngrams_list+=ngrams
            prefix_list+=prefix
    ngrams_counter=Counter(ngrams_list)
    prefix_counter=Counter(prefix_list)
    
    
    test_df=get_test(project)
    scores=[]
    for codeline in list(test_df['codelines']):
        #对生成的句子打分
        codeline=str(codeline)
        codeline = codeline.replace("\n", "").replace("\t", " ").replace("\/?", "").replace("\\", "")
        codeline = re.sub(r"[\W]", myreplace, codeline)
        codeline=codeline.split()
        score = probability(ngrams_counter,prefix_counter,codeline)
        # print(score)
        scores.append(score)
    #排序
    scores=np.array(scores).reshape(-1,1)
    scaler=preprocessing.MinMaxScaler()
    scores=scaler.fit_transform(scores)
    scores=np.array(scores).squeeze(-1)
    predict_label=[score<0.5 for score in scores]
    # print(predict_label)
    test_df['score']=scores
    test_df['predict_label']=predict_label
    
    test_df=test_df.sort_values(by='score',ascending=True)
    line_label=list(test_df["line_label"])
    line_pred=list(test_df["score"])
    line_pred=[1.0-pred for pred in line_pred]
    predict_label=list(test_df['predict_label'])
    auc=roc_auc_score(line_label,line_pred)
    aucs.append(auc)

    TP,FP,FN,TN=0,0,0,0
    for label,predict in zip(line_label,predict_label):
        if label==True and predict==True:
            TP+=1
        if label==True and predict==False:
            FP+=1
        if label==False and predict==True:
            FN+=1
        if label==False and predict==False:
            TN+=1


    recall=recall_score(line_label,predict_label)
    precision=precision_score(line_label,predict_label)
    f1=f1_score(line_label,predict_label)
    # f1=2*precision*recall/(precision+recall)
    balance_acc=(TP / (TP+FN)+TN / (TN+FP))/2.0
    mcc=matthews_corrcoef(line_label,predict_label)
    
    recalls.append(recall)
    precisions.append(precision)
    f1s.append(f1)
    balance_accs.append(balance_acc)
    mccs.append(mcc)

    #计算recall@20%LOC
    predict=[1 for _ in range(int(len(line_label)*0.2))]
    length=len(predict)
    for _ in range(len(line_label)-length):
        predict.append(0)
    
    recall_20_LOC=recall_score(line_label,predict)
    
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

    recall_20_LOCs.append(recall_20_LOC)
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

    with open(result_path+"result{}.txt".format(n),'a') as f:
        f.write(project+" recall_20_LOC: "+str(recall_20_LOC)+" effort@20%Recall: "+str(effort_20_recall)+" IFA: "+str(np.mean(IFA))+
        " balance_acc: "+str(balance_acc)+" mcc: "+str(mcc)+" f1: "+str(f1)+" precision: "+str(precision)+" recall: "+str(recall)+"\n")

dic={"projects":projects,"recall@20LOC":recall_20_LOCs,"effort@20recall":effort_20_recalls,"IFA":IFAs,"auc":aucs,"recall":recalls,"precision":precisions,"f1":f1s,"balance_acc":balance_accs,"mcc":mccs}
df=pd.DataFrame(dic)
df.to_csv(result_path+"result{}.csv".format(n),index=False)