import time
import re
import numpy as np
import os

import pandas as pd
from gensim.models.word2vec import Word2Vec
import torch
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset
from torch.utils.data import DataLoader, TensorDataset

max_seq_len = 50
delta = 5

all_datas = ['activemq', 'camel', 'derby', 'groovy', 'hbase', 'jruby', 'lucene', 'wicket']

all_train_releases = {'activemq': 'activemq-5.0.0', 'camel': 'camel-1.4.0', 'derby': 'derby-10.2.1.6',
                      'groovy': 'groovy-1_5_7', 'hbase': 'hbase-0.94.0', 'hive': 'hive-0.9.0',
                      'jruby': 'jruby-1.1', 'lucene': 'lucene-2.3.0', 'wicket': 'wicket-1.3.0-incubating-beta-1'}

all_eval_releases = {'activemq': ['activemq-5.1.0', 'activemq-5.2.0', 'activemq-5.3.0', 'activemq-5.8.0'],
                     'camel': ['camel-2.9.0', 'camel-2.10.0', 'camel-2.11.0'],
                     'derby': ['derby-10.3.1.4', 'derby-10.5.1.1'],
                     'groovy': ['groovy-1_6_BETA_1','groovy-1_6_BETA_2'],
                     'hbase': ['hbase-0.95.0', 'hbase-0.95.2'], 'hive': ['hive-0.10.0', 'hive-0.12.0'],
                     'jruby': ['jruby-1.4.0', 'jruby-1.5.0', 'jruby-1.7.0.preview1'],
                     'lucene': ['lucene-2.9.0', 'lucene-3.0.0', 'lucene-3.1'],
                     'wicket': ['wicket-1.3.0-beta2', 'wicket-1.5.3']}

all_releases = {'activemq': ['activemq-5.0.0', 'activemq-5.1.0', 'activemq-5.2.0', 'activemq-5.3.0', 'activemq-5.8.0'],
                'camel': ['camel-1.4.0', 'camel-2.9.0', 'camel-2.10.0', 'camel-2.11.0'],
                'derby': ['derby-10.2.1.6', 'derby-10.3.1.4', 'derby-10.5.1.1'],
                'groovy': ['groovy-1_5_7', 'groovy-1_6_BETA_1','groovy-1_6_BETA_2'],
                'hbase': ['hbase-0.94.0', 'hbase-0.95.0', 'hbase-0.95.2'],
                'hive': ['hive-0.9.0', 'hive-0.10.0', 'hive-0.12.0'],
                'jruby': ['jruby-1.1', 'jruby-1.4.0', 'jruby-1.5.0', 'jruby-1.7.0.preview1'],
                'lucene': ['lucene-2.3.0', 'lucene-2.9.0', 'lucene-3.0.0', 'lucene-3.1'],
                'wicket': ['wicket-1.3.0-incubating-beta-1', 'wicket-1.3.0-beta2', 'wicket-1.5.3']}

# all_releases = {'groovy': ['groovy-1_5_7', 'groovy-1_6_BETA_1','groovy-1_6_BETA_2']}

all_projs = list(all_train_releases.keys())

file_lvl_gt = '../datasets/preprocessed_data/'

word2vec_dir = '../output/Word2Vec_model/'


def get_df(rel, is_baseline=False):
    if is_baseline:
        df = pd.read_csv('../' + file_lvl_gt + rel + ".csv")

    else:
        df = pd.read_csv(file_lvl_gt + rel + ".csv")

    df = df.fillna('')

    # df = df[df['is_blank'] == False]
    df = df[df['is_test_file'] == False]

    return df


def prepare_code2d(code_list, to_lowercase=False):
    '''
        input
            code_list (list): list that contains code each line (in str format)
        output
            code2d (nested list): a list that contains list of tokens with padding by '<pad>'
    '''
    code2d = []

    for c in code_list:
        c = re.sub('\\s+', ' ', c)

        if to_lowercase:
            c = c.lower()

        token_list = c.strip().split()
        total_tokens = len(token_list)

        token_list = token_list[:max_seq_len]

        if total_tokens < max_seq_len:
            token_list = token_list + ['<pad>'] * (max_seq_len - total_tokens)

        code2d.append(token_list)

    return code2d


def get_context(df, index):
    code = []
    start = max(index - delta, df.index.min())
    # end = min(index + delta, df.index.max())

    for i in range(start, index+1):
        code.append(df.iloc[i]['code_line'])
    # label = df.iloc[index]['Bug']
    return code
    # return start, end


def get_code3d_and_label(df, to_lowercase=False):
    '''
        input
            df (DataFrame): a dataframe from get_df()
        output
            code3d (nested list): a list of code2d from prepare_code2d()
            all_file_label (list): a list of file-level label
    '''

    code3d = []
    all_lines_label = []

    for filename, group_df in df.groupby('filename'):
        group_df = group_df.reset_index().drop('index', axis=1)
        code = list(group_df['code_line'])
        a = group_df.index
        # group_df['context']=pd.Series([get_context(group_df,i) for i in a])
        codes = list([get_context(group_df, i) for i in a])
        for code in codes:
            code2d = prepare_code2d(code, to_lowercase)
            code3d.append(code2d)
    all_lines_label=[bool(i) for i in list(df['line-label'])]
    return code3d, all_lines_label


def get_w2v_path():
    return word2vec_dir


def get_w2v_weight_for_deep_learning_models(word2vec_model, embed_dim,device):
    word2vec_weights = torch.FloatTensor(word2vec_model.wv.syn0).to(device)

    # add zero vector for unknown tokens
    word2vec_weights = torch.cat((word2vec_weights, torch.zeros(1, embed_dim).to(device)))

    return word2vec_weights


def pad_code(code_list_3d, max_sent_len, limit_sent_len=True, mode='train'):
    paded = []

    for file in code_list_3d:
        sent_list = []
        for line in file:
            new_line = line
            if len(line) > max_seq_len:
                new_line = line[:max_seq_len]
            sent_list.append(new_line)

        if mode == 'train':
            if max_sent_len - len(file) > 0:
                for i in range(0, max_sent_len - len(file)):
                    sent_list.append([0] * max_seq_len)

        if limit_sent_len:
            paded.append(sent_list[:max_sent_len])
        else:
            paded.append(sent_list)

    return paded


def get_dataloader(code_vec, label_list, batch_size, max_sent_len):
    y_tensor = torch.FloatTensor([label for label in label_list])
    code_vec_pad = pad_code(code_vec, max_sent_len)
    tensor_dataset = TensorDataset(torch.tensor(code_vec_pad), y_tensor)

    dl = DataLoader(tensor_dataset, shuffle=True, batch_size=batch_size, drop_last=True)

    return dl


def get_x_vec(code_3d, word2vec):
    x_vec = [
        [[word2vec.wv.vocab[token].index if token in word2vec.wv.vocab else len(word2vec.wv.vocab) for token in text]
         for text in texts] for texts in code_3d]

    return x_vec


class DataPrefetcher():
    def __init__(self, loader, device):
        self.loader = iter(loader)
        self.device = device
        self.stream = torch.cuda.Stream()
        self.preload()

    def preload(self):
        try:
            self.text, self.label = next(self.loader)
        except StopIteration:
            self.text, self.label = None, None
            return
        with torch.cuda.stream(self.stream):
            self.text = self.text.cuda(non_blocking=False)
            self.label = self.label.cuda(non_blocking=False)

    def next(self):
        torch.cuda.current_stream().wait_stream(self.stream)
        text = self.text
        label = self.label
        self.preload()
        return text, label


def extract_tokens(s):
    s = re.sub("/\*.*?\*/", '', s, flags=re.DOTALL)
    s = re.sub("//.*?\n", '\n', s)
    lst = re.sub("[^a-zA-Z0-9\s]", ' ', s).split()
    return [s for s in lst if len(re.sub("^[0-9]+$|^\w$", '', s)) > 1]


class SourceCodeData():
    def __init__(self, release, embedding_size, delta=5):
        start_time = time.time()
        print(f'Loading {release} ...')
        self.delta = delta
        self.df = pd.read_csv(f'../Dataset/extracted-source-code/{release}.csv')
        # self.df = pd.read_pickle(f'../Dataset/data/{release}.pkl')
        self.df['SRC'] = self.df['SRC'].apply(lambda s: extract_tokens(s))
        self.df = self.df.drop(self.df['SRC'][self.df['SRC'].apply(lambda x: not x)].index).reset_index().drop('index',
                                                                                                               axis=1)
        try:
            self.model = Word2Vec.load(f'../model/{release}.w2v')
        except FileNotFoundError:
            self.model = Word2Vec(sentences=self.df['SRC'], min_count=1, sg=1, vector_size=embedding_size,
                                  workers=int(os.cpu_count() * 0.9))
            self.model.save(f'../model/{release}.w2v')
        # self.df['embedding'] = self.df['SRC'].apply(lambda v : np.mean([self.model.wv[x] for x in v], axis=0))
        self.df['embedding'] = self.df['SRC'].apply(lambda v: self.model.wv[v])
        self.df['Bug'] = self.df['Bug'].astype(int).apply(lambda x: np.array(x))
        self.bug_list = self.df[self.df['Bug'] == 1].reset_index().drop('index', axis=1)
        self.no_bug_list = self.df[self.df['Bug'] == 0].reset_index().drop('index', axis=1)

        # 切分训练集和测试集，8：2
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.df['embedding'], self.df['Bug'],
                                                                                test_size=0.2, stratify=self.df['Bug'])
        # 将测试集再分一半给验证集
        self.x_valid, self.x_test, self.y_valid, self.y_test = train_test_split(self.x_test, self.y_test,
                                                                                test_size=0.5, stratify=self.y_test)

        self.x_train = self.x_train.reset_index().drop('index', axis=1)
        self.y_train = self.y_train.reset_index().drop('index', axis=1)
        self.x_test = self.x_test.reset_index().drop('index', axis=1)
        self.y_test = self.y_test.reset_index().drop('index', axis=1)
        self.x_valid = self.x_valid.reset_index().drop('index', axis=1)
        self.y_valid = self.y_valid.reset_index().drop('index', axis=1)
        print(f'{release} loaded in {time.time() - start_time} s.')

    def __getitem__(self, index):

        embedding = self.df.iloc[index]['embedding']
        # embedding = self.df.iloc[range(start,end)]['embedding']
        label = self.df.iloc[index]['Bug']
        return embedding, [label]

    def __len__(self):
        return self.df.shape[0]

    def get_train_test(self):
        train, valid, test = [], [], []
        for i in range(len(self.x_train)):
            train.append([self.x_train.iloc[i]['embedding'], [self.y_train.iloc[i]['Bug']]])
        for i in range(len(self.x_valid)):
            valid.append([self.x_valid.iloc[i]['embedding'], [self.y_valid.iloc[i]['Bug']]])
        for i in range(len(self.x_test)):
            test.append([self.x_test.iloc[i]['embedding'], [self.y_test.iloc[i]['Bug']]])
        return train, valid, test


class Embedding_Loader():
    def __init__(self, release):
        start_time = time.time()
        print(f'Loading {release} ...')

        self.df = pd.read_pickle(f'../Dataset/data/{release}.pkl')
        # 切分训练集和测试集，8：2

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.df['embedding_context'],
                                                                                self.df['Bug'],
                                                                                test_size=0.2, stratify=self.df['Bug'])
        # 将测试集再分一半给验证集
        self.x_valid, self.x_test, self.y_valid, self.y_test = train_test_split(self.x_test, self.y_test,
                                                                                test_size=0.5, stratify=self.y_test)

        self.x_train = self.x_train.reset_index().drop('index', axis=1)
        self.y_train = self.y_train.reset_index().drop('index', axis=1)
        self.x_test = self.x_test.reset_index().drop('index', axis=1)
        self.y_test = self.y_test.reset_index().drop('index', axis=1)
        self.x_valid = self.x_valid.reset_index().drop('index', axis=1)
        self.y_valid = self.y_valid.reset_index().drop('index', axis=1)
        print(f'{release} loaded in {time.time() - start_time} s.')

    def __getitem__(self, index):

        embedding = self.df.iloc[index]['embedding_context']
        # embedding = self.df.iloc[range(start,end)]['embedding']
        label = self.df.iloc[index]['Bug']
        return embedding, [label]

    def __len__(self):
        return self.df.shape[0]

    def get_train_test(self):
        train, valid, test = [], [], []
        for i in range(len(self.x_train)):
            train.append([self.x_train.iloc[i]['embedding_context'], [self.y_train.iloc[i]['Bug']]])
        for i in range(len(self.x_valid)):
            valid.append([self.x_valid.iloc[i]['embedding_context'], [self.y_valid.iloc[i]['Bug']]])
        for i in range(len(self.x_test)):
            test.append([self.x_test.iloc[i]['embedding_context'], [self.y_test.iloc[i]['Bug']]])
        return train, valid, test
