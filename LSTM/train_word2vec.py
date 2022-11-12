import os,sys
from gensim.models import Word2Vec
import numpy as np
import more_itertools
import pandas as pd

corpus_path="../Datasets/preprocessed_data3/"
w2v_path="../LSTM/word2vec/"
if not os.path.exists(w2v_path):
    os.makedirs(w2v_path)
all_releases = {'activemq': ['activemq-5.0.0', 'activemq-5.1.0', 'activemq-5.2.0', 'activemq-5.3.0', 'activemq-5.8.0'],
                     'camel': ['camel-1.4.0', 'camel-2.9.0', 'camel-2.10.0', 'camel-2.11.0'],
                     'derby': ['derby-10.2.1.6', 'derby-10.3.1.4', 'derby-10.5.1.1'],
                     'groovy': ['groovy-1_5_7', 'groovy-1_6_BETA_1', 'groovy-1_6_BETA_2'],
                     'hbase': ['hbase-0.94.0', 'hbase-0.95.0', 'hbase-0.95.2'], 'hive': ['hive-0.9.0', 'hive-0.10.0', 'hive-0.12.0'],
                     'jruby': ['jruby-1.1', 'jruby-1.4.0', 'jruby-1.5.0', 'jruby-1.7.0.preview1'],
                     'lucene': ['lucene-2.3.0', 'lucene-2.9.0', 'lucene-3.0.0', 'lucene-3.1'],
                     'wicket': ['wicket-1.3.0-incubating-beta-1', 'wicket-1.3.0-beta2', 'wicket-1.5.3']}

def get_data(project):
    train_file=all_releases[project][0]
    data=[]
    df=pd.read_csv(corpus_path+train_file+".csv")
    for ast in list(df['ast']):
        ast=ast[1:-1].replace(" ","").replace("\'","").split(",")
        data.append(ast)
    return data

def train_word2vec_model(dataset_name,embedding_dim=50):

    save_path=w2v_path+'/'+dataset_name+'-'+str(embedding_dim)+'dim.bin'

    if os.path.exists(save_path):
        print('word2vec model at {} is already exits'.format(save_path))
        return

    train_data=get_data(dataset_name)

    word2vecdir=Word2Vec(train_data,size=embedding_dim,min_count=1,sorted_vocab=1)


    word2vecdir.save(save_path)

    print('save word2vec model at path {} done'.format(save_path))

# p=sys.argv[1]
for p in ['activemq', 'camel', 'derby','groovy', 'hbase', 'hive','jruby', 'lucene', 'wicket']:
    train_word2vec_model(p,500)