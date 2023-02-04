import random
import pandas as pd
import numpy as np
import subprocess, re, os, time
import re
from xml.dom.minidom import parse

from multiprocessing import Pool

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

# all_eval_releases = ['hbase-0.95.2',
#                      'hive-0.12.0',
#                      'jruby-1.5.0','jruby-1.7.0.preview1',
#                      'lucene-3.0.0','lucene-3.1', 
#                      'wicket-1.5.3']

all_dataset_name = ['activemq','camel','derby','groovy','hbase','hive','jruby','lucene','wicket']

base_file_dir = './PMD_data/'
base_command = "bash ./pmd-bin-6.53.0/bin/run.sh pmd -d ./PMD_data/{} -f xml -r ./xml_result/{}.xml -R rulesets/java/unusedcode.xml"

result_dir = './result/'

if not os.path.exists(result_dir):
    os.makedirs(result_dir)


def run_ErrorProne(rel):
    df_list = []
    java_file_dir = base_file_dir+rel+'/'

    file_list = os.listdir(java_file_dir)
    
    data_df=pd.read_csv("./data/"+rel+".csv")
    
    # os.system("bash ./pmd-bin-6.53.0/bin/run.sh pmd -d ./PMD_data/activemq-5.2.0 -f xml -r ./result/result.xml -R rulesets/java/unusedcode.xml")
    
    os.system(base_command.format(rel,rel))
    domtree=parse("./xml_result/{}.xml".format(rel))

    data=domtree.documentElement
    defective_file_list=[]
    for i,file in enumerate(data.getElementsByTagName("file")):
        print(i,file.getAttribute("name"))
        java_filename=str(file.getAttribute("name"))
        defective_file=java_filename[java_filename.rfind('/')+1:]
        defective_file_list.append(defective_file)
        defective_lines=[]
        for violation in file.getElementsByTagName("violation"):
                defective_lines.append(int(violation.getAttribute("beginline")))
        
        criteria=(data_df['filename']==defective_file)
        line_label=list(data_df[criteria]['line-label'])
        
        f = open(java_file_dir+defective_file,'r',encoding='utf-8',errors='ignore')
        java_code = f.readlines()

        code_len = len(java_code)
        # code=java_code.split("\n")

        line_df = pd.DataFrame()
        
        predict=[]

        line_df['filename'] = [defective_file]*code_len
        line_df['test-release'] = [rel]*len(line_df)
        line_df['code']=java_code
        line_df['line_number'] = np.arange(1,code_len+1)
        line_df['line_label']=line_label
        line_df['PMD_prediction_result'] = line_df['line_number'].isin(defective_lines)
        for i in line_df['PMD_prediction_result']:
            if i :
                predict.append(1+random.random())
            else:
                predict.append(random.random())
        line_df['probability']=predict
                

        df_list.append(line_df)
        

    for java_filename in tqdm(file_list):
        # print(java_filename.replace('_','/'))   
        if java_filename in defective_file_list:
            continue   
        f = open(java_file_dir+java_filename,'r',encoding='utf-8',errors='ignore')
        java_code = f.readlines()

        
        code_len = len(java_code)
        # print(code_len)

        # os.system(base_command.format(java_file_dir,java_filename))

        # domtree=parse("./result/result.xml")

        # data=domtree.documentElement

        
        defective_lines=[]
        predict=[]
        
        # for i,file in enumerate(data.getElementsByTagName("file")):
        #     print(i,file.getAttribute("name"))
        #     for violation in file.getElementsByTagName("violation"):
        #         defective_lines.append(int(violation.getAttribute("beginline")))
        
        # reported_lines = re.findall('\d+: error:',output)
        # reported_lines = [int(l.replace(':','').replace('error','')) for l in reported_lines]
        # reported_lines = list(set(reported_lines))

        criteria=(data_df['filename']==java_filename)
        line_label=list(data_df[criteria]['line-label'])

        line_df = pd.DataFrame()

        line_df['filename'] = [java_filename]*code_len
        line_df['test-release'] = [rel]*len(line_df)
        line_df['code']=java_code
        line_df['line_number'] = np.arange(1,code_len+1)
        line_df['line_label']=line_label
        line_df['PMD_prediction_result'] = line_df['line_number'].isin(defective_lines)

        for i in line_df['PMD_prediction_result']:
            if i :
                predict.append(1+random.random())
            else:
                predict.append(random.random())
        line_df['probability']=predict
        
        df_list.append(line_df)

    final_df = pd.concat(df_list)
    final_df.to_csv(result_dir+rel+'-line-lvl-result.csv',index=False)
    print('finished',rel)

for rel in all_eval_releases:
    run_ErrorProne(rel)