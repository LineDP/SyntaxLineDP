from utils import *
import pandas as pd
import random
from cmath import sqrt
from sklearn.metrics import recall_score,precision_score,f1_score,roc_auc_score,matthews_corrcoef

projects=['activemq', 'camel', 'derby', 'groovy', 'hbase', 'hive','jruby', 'lucene', 'wicket']



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

    releases=all_eval_releases[project][1:]

    df_list=[]
    
    for rel in releases:
        df=pd.read_csv("../Datasets/preprocessed_data3/{}.csv".format(rel))
        filename=list(df['filename'])
        new_filename=[rel+item for item in filename]
        df['filename']=new_filename
        df_list.append(df)
    
    df=pd.concat(df_list)
    labels=df['line_label'].tolist()
    probs=[np.mean([random.random() for _ in range(100)]) for _ in range(len(labels))]
    predicts=[prob>0.5 for prob in probs]
    df['predict']=predicts
    df['prob']=probs
    auc=roc_auc_score(labels,probs)
    aucs.append(auc)
    TP,FP,FN,TN=0,0,0,0
    for label,predict in zip(labels,predicts):
        if label==True and predict==True:
            TP+=1
        if label==True and predict==False:
            FP+=1
        if label==False and predict==True:
            FN+=1
        if label==False and predict==False:
            TN+=1
    
    recall=recall_score(labels,predicts)
    precision=precision_score(labels,predicts)
    f1=f1_score(labels,predicts)
    # f1=2*precision*recall/(precision+recall)
    balance_acc=(TP / (TP+FN)+TN / (TN+FP))/2.0
    mcc=matthews_corrcoef(labels,predicts)

    recalls.append(recall)
    precisions.append(precision)
    f1s.append(f1)
    balance_accs.append(balance_acc)
    mccs.append(mcc)

    df=df.sort_values(by='prob',ascending=False)
    line_label=list(df["line_label"])
    line_pred=list(df["prob"])
    
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

    IFA=[]
    df = df.drop(index=df[df['file_label'] == False].index).reset_index().drop('index', axis=1)
    for file,df_ in df.groupby("filename"):
        df_=df_.sort_values(by='prob',ascending=False)
        labels=list(df_['line_label'])
        for index,label in enumerate(labels):
            if label==1:
                IFA.append(index+1)
                break
    IFAs.append(np.mean(IFA))

dic={"projects":projects,"recall@20LOC":recall_20_LOCs,"effort@20recall":effort_20_recalls,"IFA":IFAs,"auc":aucs,"recall":recalls,"precision":precisions,"f1":f1s,"balance_acc":balance_accs,"mcc":mccs}
df=pd.DataFrame(dic)
df.to_csv("result.csv",index=False)
