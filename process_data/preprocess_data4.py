#统计每个release中的ast特征平均表现

import os
import json
import pandas as pd
from numpy import*
input_path="../Datasets/preprocessed_data3/"
output_path="../Datasets/preprocessed_data4/"

if not os.path.exists(output_path):
    os.makedirs(output_path)
files=os.listdir(input_path)

statements=['IfStatement','SimpleName','InfixExpression','Assignment','ExpressionStatement','Block','MethodInvocation']

for file in files:
    features={'ast_len':[],'IfStatement':[],'SimpleName':[],'InfixExpression':[],'Assignment':[],'ExpressionStatement':[],'Block':[],'MethodInvocation':[]}
    df=pd.read_csv(input_path+file)
    ast=list(df['ast'])
    line_label=list(df['line_label'])
    for a,label in zip(ast,line_label):
        data=[i.replace(' ','').replace('\'','') for i in a[1:-1].split(',')]
        features['ast_len'].append(0 if a=='[]' else len(data))
        for statement in statements:
            features[statement].append(data.count(statement))
    for key in features.keys():
        df[key]=features[key]
    df.to_csv(output_path+file,index=False)