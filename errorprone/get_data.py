import pandas as pd
import numpy as np
import subprocess,re, os, time


from tqdm import tqdm

all_eval_releases = ['activemq-5.2.0','activemq-5.3.0','activemq-5.8.0',
                     'camel-2.10.0','camel-2.11.0', 
                     'derby-10.5.1.1',
                     'groovy-1_6_BETA_2', 
                     'hbase-0.95.2',
                     'hive-0.12.0', 
                     'jruby-1.5.0','jruby-1.7.0.preview1',
                     'lucene-3.0.0','lucene-3.1', 
                     'wicket-1.5.3']

all_dataset_name = ['activemq','camel','derby','groovy','hbase','hive','jruby','lucene','wicket']

base_file_dir = './data/'
base_command = "javac -J-Xbootclasspath/p:javac-9+181-r4173-1.jar -XDcompilePolicy=simple -processorpath error_prone_core-2.4.0-with-dependencies.jar:dataflow-shaded-3.1.2.jar:jFormatString-3.0.0.jar '-Xplugin:ErrorProne -XepDisableAllChecks -Xep:CollectionIncompatibleType:ERROR' "

errorprone_data='./errorprone_data/'

result_dir = './result/'

if not os.path.exists(result_dir):
    os.makedirs(result_dir)


for rel in all_eval_releases:

    data_df=pd.read_csv(base_file_dir+rel+".csv")
    rel_dir=errorprone_data+rel+"/"

    if not os.path.exists(rel_dir):
        os.makedirs(rel_dir)

    df_list=[]
    for filename,df in tqdm(data_df.groupby("filename")):
        code_len=len(list(df['code_line']))
        lines=""
        for line in list(df['code_line']):
            lines+=str(line)+"\n"
        with open(rel_dir+filename,"w") as f:
            f.write(lines)