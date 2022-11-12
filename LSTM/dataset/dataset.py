from copy import copy
import json
import os
import re
import copy
from pickle import FALSE, TRUE
import torch
import pandas as pd
import numpy as np
from torch.utils.data import Dataset

class BiLSTMDataset(Dataset):
    #词典，文件列表list，输出的长度
    def __init__(self, word2vec,corpus_path, corpus_files, code_len,Train=True):
        self.word2vec = word2vec
        self.files = corpus_files
        self.code_len=code_len
        self.corpus_lines = 0
        self.filename=[]
        self.file_label=[]
        self.ast=[]
        self.label=[]
        self.buggy_filename=[]
        self.buggy_file_label=[]
        self.buggy_ast=[]
        self.index=0
        for index, tmp_file in enumerate(self.files):
            df=pd.read_csv(corpus_path+tmp_file+".csv")
            for filename,ast,file_label,label in zip(list(df['filename']),list(df['ast']),list(df['file_label']),list(df['line_label'])):
                # if Train==False and file_label==False:
                #     continue             
                if ast=='[]':
                    continue
                self.filename.append(tmp_file+filename)
                self.file_label.append(file_label)
                self.ast.append(ast)
                self.label.append(label)
                if label:
                    self.buggy_filename.append(tmp_file+filename)
                    self.buggy_file_label.append(file_label)
                    self.buggy_ast.append(ast)
        
        #如果是训练集数据，需要作不均衡处理
        if Train:
            print("不平衡处理前\n")
            print(self.label.count(True))
            print(self.label.count(False))
            # while self.label.count(True)<self.label.count(False):
            for _ in range(self.label.count(False)-self.label.count(True)):
                self.filename.append(self.buggy_filename[self.index])
                self.file_label.append(self.buggy_file_label[self.index])
                self.ast.append(self.buggy_ast[self.index])
                self.label.append(True)
                self.index=(self.index+1)%len(self.buggy_ast)
            
            print("不平衡处理后\n")
            print(self.label.count(True))
            print(self.label.count(False))
        
        self.corpus_lines =len(self.ast)
        self.line_index=0

    def __len__(self):
        return self.corpus_lines
    
    def __getitem__(self, item):
        # print("start getdata")
        #获取代码行的ast以及标签
        filename,file_label,ast, label = self.get_corpus_line()
        #对代码行的ast进行截断
        ast=ast[:self.code_len]
        
        #根据词典对每个ast结点取下标
        for i,node in enumerate(ast):
            # ast[i]=self.vocab.stoi.get(node.lower() + '</w>', self.vocab.unk_index)
            ast[i]=self.word2vec[node] if node in self.word2vec.wv.vocab else [0.0 for _ in range(500)]
        
        #对ast添加padding补长
        padding = [[0.0 for i in range(500)] for _ in range(self.code_len - len(ast))]
        ast.extend(padding)
        ast=np.array(ast)
        # sos_token = self.vocab.sos_index_java
        # ast = [sos_token] + ast + [self.vocab.cls_index]
        # code = code + [self.vocab.cls_index] + [self.vocab.eos_index]
        
        output = {"filename":filename,
                  "file_label":file_label,
                  "ast_input": torch.tensor(ast).float(),
                  "is_defect": torch.tensor(label).float()}
        
        return output

    def get_corpus_line(self):
        
        filename=self.filename[self.line_index]
        file_label=self.file_label[self.line_index]
        line=[node.replace(" ","").replace("\'","") for node in self.ast[self.line_index][1:-1].split(",")]
        
        label=self.label[self.line_index]
        self.line_index=(self.line_index+1)%self.corpus_lines
        return filename,file_label,line, label
