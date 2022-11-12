import json
import pandas as pd
import os, re
import numpy as np
from tqdm import tqdm

from utils import *

data_root_dir = '../Datasets/original/'
input = '../Datasets/codewithast/'
output='../Datasets/preprocessed_data3/'

if not os.path.exists(output):
    os.makedirs(output)

dirty_df=pd.DataFrame()
releases=[]

def preprocess_data(proj_name):
    global dirty_df
    cur_all_rel = all_releases[proj_name]

    for rel in cur_all_rel:
        
        InFile=open(input+rel+".txt",'r')
        filename,is_test_file,codelines,ast,file_label,line_label,line_number=[],[],[],[],[],[],[]
        for item in InFile.readlines():
            data=json.loads(item)
            filename.extend(data["filename"])
            is_test_file.extend(data['is_test_file'])
            codelines.extend(data['codelines'])
            ast.extend(data['ast'])
            file_label.extend(data['file_label'])
            line_label.extend(data['line_label'])
            line_number.extend(data['line_number'])
            
        dict={"filename":filename,"is_test_file":is_test_file,"codelines":codelines,"ast":ast,"file_label":file_label,"line_label":line_label,"line_number":line_number}
        df=pd.DataFrame(dict)
        df.to_csv(output+rel+".csv",index=False)
        print('finish release {}'.format(rel))
        InFile.close()
for proj in list(all_releases.keys()):
    preprocess_data(proj)
