import json
import pandas as pd
import os, re
import numpy as np
from tqdm import tqdm

from utils import *

data_root_dir = '../Datasets/original/'
input = '../Datasets/preprocessed_data/'
output='../Datasets/preprocessed_data2/'

if not os.path.exists(output):
    os.makedirs(output)

dirty_df=pd.DataFrame()
releases=[]

def get_newfile(filenames):
    newfilenames=[]
    for i in filenames:
        if i not in newfilenames:
            newfilenames.append(i)
    return newfilenames

def preprocess_data(proj_name):
    global dirty_df
    cur_all_rel = all_releases[proj_name]

    for rel in cur_all_rel:
        with open(output+rel+".txt",'w') as f:
            df=pd.read_csv(input+rel+'.csv',encoding='latin')
            for filename, df in tqdm(df.groupby('filename')):
                file=list(df['filename'])
                codelines=list(df['code_line'])
                is_test_file=list(df['is_test_file'])
                file_label=list(df['file-label'])
                line_label=list(df['line-label'])
                line_number=list(df['line_number'])
                
                Dict={"filename":file,"codelines":codelines,"is_test_file":is_test_file,"file_label":file_label,"line_label":line_label,"line_number":line_number}
                json_str=json.dumps(Dict)
                f.write(json_str+"\n")
            # df.to_excel(output + rel + ".xlsx", index=False,engine='xlsxwriter')
            print('finish release {}'.format(rel))

for proj in list(all_releases.keys()):
    preprocess_data(proj)
