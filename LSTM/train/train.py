from cmath import sqrt
import json
from statistics import mean
import sys
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim import Adam
from tqdm import tqdm
from sklearn.metrics import roc_auc_score
from .optim_schedule import ScheduledOptim
from sklearn.metrics import recall_score,precision_score,f1_score,matthews_corrcoef
from train.focal_loss import BinaryFocalLoss
# from model.linedp import LineDP


class Trainer:
    def __init__(self, model, alpha, train_dataloader: DataLoader,
                 test_dataloader: DataLoader = None, lr: float = 1e-4, betas=(0.9, 0.999), weight_decay: float = 0.01,
                 warmup_steps=10000, device=None, log_freq: int = 10):
        self.alpha = alpha
        
        self.device = device
        self.model = model.to(self.device)
        # self.model = LineDP(self.transformer, target=1).to(self.device)

        # if with_cuda and torch.cuda.device_count() > 1:
        #     print("Using %d GPUs for LineDP" % torch.cuda.device_count())
        #     self.model = nn.DataParallel(self.model, device_ids=[0,1])

        self.train_data = train_dataloader
        self.test_data = test_dataloader

        self.optim = Adam(self.model.parameters(), lr=lr, betas=betas, weight_decay=weight_decay)
        # self.optim_schedule = ScheduledOptim(self.optim, self.transformer.hidden, n_warmup_steps=warmup_steps)

        # self.criterion=BinaryFocalLoss(0.5,2,'mean')
        self.criterion=nn.BCELoss()
        self.log_freq = log_freq

        print("Total Parameters:", sum([p.nelement() for p in self.model.parameters()]))

    def train(self, epoch):
        loss,_,__= self.iteration(epoch, self.train_data, train=True)   
        return loss

    def test(self, epoch):  
        loss ,attention_dict,line_result= self.iteration(epoch, self.test_data, train=False)
        return line_result

    def iteration(self, epoch, data_loader, train=True):
        str_code = "train" if train else "test"
        data_iter = tqdm(enumerate(data_loader),
                         desc="EP_%s:%d" % (str_code, epoch),
                         total=len(data_loader),
                         bar_format="{l_bar}{r_bar}")
        avg_loss = 0.0
        total_correct = 0
        total_element = 0
        # pre_positive=0
        positive=0
        negetive=0
        TP=0.0
        FN=0.0
        FP=0.0
        TN=0.0
        filename=[]
        file_label=[]
        line_label=[]
        line_pred=[]
        predict_label=[]
        AUC=0.0

        # print(self.device)
        attention_dict={}
        line_result={}
        
        for i, data in data_iter:
            # print(data)
            # data = {key: value.to(self.device) for key, value in data.items()}
            torch.cuda.empty_cache()
            targets = self.model.forward(data["ast_input"].to(self.device))
            torch.cuda.empty_cache()
            # print("code_token:",code_token)
            # loss = self.criterionTarget(targets.squeeze(dim=-1), data["is_defect"].float())
            loss = self.criterion(targets.squeeze(dim=-1), data["is_defect"].to(self.device).float())
            # loss2=self.criterionToken(attention.squeeze(dim=-1),nn.LogSoftmax(data["count_num"]).squeeze(dim=-1))
            # loss=loss1

            if train:
                # self.optim_schedule.zero_grad()
                self.model.zero_grad()
                loss.backward()
                self.optim.step()
                # self.optim_schedule.step_and_update_lr()
                      
            target_prediction = (targets > 0.9).squeeze(-1)
            predict_label.extend(target_prediction)
            filename.extend(data["filename"])
            file_label.extend(data["file_label"])
            line_label.extend(data["is_defect"].cpu().numpy().tolist())
            line_pred.extend(targets.squeeze(dim=-1).cpu().detach().numpy().tolist())
            # correct = target_prediction.eq(data["is_defect"]).sum().item()
            avg_loss += loss.item()
            # total_correct += correct
            # total_element+=data["is_defect"].nelement()
            # positive+=data["is_defect"].cpu().numpy().tolist().count(1)
            # negetive+=data["is_defect"].cpu().numpy().tolist().count(0)
            
        for label,predict in zip(line_label,predict_label):
            if label==1 and predict==1:
                TP+=1
            if label==0 and predict==1:
                FP+=1
            if label==1 and predict==0:
                FN+=1
            if label==0 and predict==0:
                TN+=1
        try:        
            if train==False:
                try:
                    AUC=roc_auc_score(line_label,line_pred)
                    precision=TP/(TP+FP)
                    recall=TP/(TP+FN)
                    f1=2*precision*recall/(precision+recall)
                    balance_acc=(TP / (TP+FN)+TN / (TN+FP))/2.0
                    mcc=matthews_corrcoef(line_label,predict_label)
                except:
                    AUC=0
                    balance_acc=0
                    mcc=0
                    precision=0
                    recall=0
                    f1=0
                line_result["auc"]=AUC
                line_result["balance_acc"]=balance_acc
                line_result["mcc"]=mcc
                line_result["f1"]=f1
                line_result["precision"]=precision
                line_result["recall"]=recall

                df=pd.DataFrame()
                df["filename"]=filename
                df["file_label"]=file_label
                df["line_label"]=line_label
                df["line_pred"]=line_pred
                df=df.sort_values(by='line_pred',ascending=False)
                line_label=list(df["line_label"])
                line_pred=list(df["line_pred"])
                
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
                line_result["recall@20%LOC"]=recall_20_LOC
                line_result["effort@20%Recall"]=effort_20_recall
                
                #计算IFA，计算范围是有缺陷的文件
                IFA=[]
                df = df.drop(index=df[df['file_label'] == False].index).reset_index().drop('index', axis=1)
                for file,df_ in df.groupby("filename"):
                    df_=df_.sort_values(by='line_pred',ascending=False)
                    labels=list(df_['line_label'])
                    for index,label in enumerate(labels):
                        if label==1:
                            IFA.append(index+1)
                            break
                line_result["IFA"]=np.mean(IFA)
                        
                
                print("EP%d_%s, avg_loss=" % (epoch, str_code), avg_loss / len(data_iter),"recall@20%LOC=",recall_20_LOC,"effort@20%Recall=",effort_20_recall)
            else:    
                print("EP%d_%s, avg_loss=" % (epoch, str_code), avg_loss / len(data_iter), ", balance acc=",(TP / (TP+FN)+TN / (TN+FP))/2.0,
                      ", mcc=",(TP*TN-FP*FN)/sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)))
        except:
            print("EP%d_%s, avg_loss=" % (epoch, str_code), avg_loss / len(data_iter))
        print(" TP:",TP," FP:",FP," FN:",FN," TN:",TN)
        return avg_loss / len(data_iter),attention_dict,line_result

    def save(self, epoch, file_path="output/trained.model"):
        output_path = file_path + ".ep%d" % epoch
        torch.save(self.model, output_path)
        print("EP:%d Model Saved on:" % epoch, output_path)
        return output_path