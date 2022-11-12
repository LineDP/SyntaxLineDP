import argparse
from asyncore import write
import copy
from platform import release
from numpy import append
import torch
import json
import os
import pandas as pd
from torch.utils.data import DataLoader
from model.bilstm import Bilstm
from model.cnn import TextCNN
from gensim.models import Word2Vec
from dataset import BPE,TokenVocab, BiLSTMDataset
from train import Trainer

Syntax_nodes=["IfStatement", "SimpleName", "InfixExpression", "Assignment", "Expression", "Block", "MethodInvocation"]
Syntax_node="MethodInvocation"
projects=['activemq','camel','derby','groovy','hbase','hive','jruby','lucene','wicket']

RQ_path="../LSTM/Discussion/remove_{}/".format(Syntax_node)

word2vec_path="../LSTM/word2vec/"

if not os.path.exists(RQ_path):
    os.makedirs(RQ_path)

all_releases = {'activemq': ['activemq-5.0.0', 'activemq-5.1.0', 'activemq-5.2.0', 'activemq-5.3.0', 'activemq-5.8.0'],
                'camel': ['camel-1.4.0', 'camel-2.9.0', 'camel-2.10.0', 'camel-2.11.0'],
                'derby': ['derby-10.2.1.6', 'derby-10.3.1.4', 'derby-10.5.1.1'],
                'groovy': ['groovy-1_5_7', 'groovy-1_6_BETA_1', 'groovy-1_6_BETA_2'],
                'hbase': ['hbase-0.94.0', 'hbase-0.95.0', 'hbase-0.95.2'],
                'hive': ['hive-0.9.0', 'hive-0.10.0', 'hive-0.12.0'],
                'jruby': ['jruby-1.1', 'jruby-1.4.0', 'jruby-1.5.0', 'jruby-1.7.0.preview1'],
                'lucene': ['lucene-2.3.0', 'lucene-2.9.0', 'lucene-3.0.0', 'lucene-3.1'],
                'wicket': ['wicket-1.3.0-incubating-beta-1', 'wicket-1.3.0-beta2', 'wicket-1.5.3']}

def train():
    parser = argparse.ArgumentParser()
    parser.add_argument("-td", "--train_dataset", type=str, help="train set")
    parser.add_argument("-vd", "--valid_dataset", type=str, default=None, help="validation set")
    parser.add_argument("-v", "--vocab_path", type=str, help="vocab path")
    parser.add_argument("-pm", "--pretrain_model", type=str, help="vocab path")
    parser.add_argument("-o", "--output_path", type=str, help="model save path")
    parser.add_argument("-fs", "--feed_forward_hidden", type=int, default=3072,
                        help="hidden size of feed-forward network")
    parser.add_argument("-aj", "--attention_json", type=str, help="attention_json")
    parser.add_argument("-hs", "--hidden", type=int, default=768, help="hidden size of transformer model")
    parser.add_argument("-l", "--layers", type=int, default=12, help="number of transformer layers")
    parser.add_argument("-a", "--attn_heads", type=int, default=12, help="number of attention heads")
    parser.add_argument("-p", "--path_num", type=int, default=100, help="a AST's maximum path num")
    parser.add_argument("-n", "--node_num", type=int, default=20, help="a path's maximum node num")
    parser.add_argument("-c", "--code_len", type=int, default=200, help="maximum code len")

    parser.add_argument("-al", "--alpha", type=int, default=0.75, help="loss weight")
    parser.add_argument("-b", "--batch_size", type=int, default=1024, help="number of batch_size")
    parser.add_argument("-e", "--epochs", type=int, default=20, help="number of epochs")
    parser.add_argument("-w", "--num_workers", type=int, default=0, help="dataloader worker num")

    parser.add_argument("--with_cuda", type=bool, default=True, help="training with CUDA: true, or false")
    parser.add_argument("--log_freq", type=int, default=10, help="printing loss every n iter: setting n")
    parser.add_argument("--corpus_lines", type=int, default=None, help="total number of lines in corpus")
    parser.add_argument("--cuda_devices", type=int, nargs='+', default=None, help="CUDA device ids")

    parser.add_argument("--lr", type=float, default=1e-5, help="learning rate of adam")
    parser.add_argument("--adam_weight_decay", type=float, default=0.01, help="weight_decay of adam")
    parser.add_argument("--adam_beta1", type=float, default=0.9, help="adam first beta value")
    parser.add_argument("--adam_beta2", type=float, default=0.999, help="adam first beta value")

    args = parser.parse_args()

    print("Loading Vocab", args.vocab_path)
    
    data_path="../Datasets/discussion/remove_{}/".format(Syntax_node)
    
    for project in projects:
        
        word2vec_file_dir = os.path.join(word2vec_path, project + '-' + str(500) + 'dim.bin')
        word2vec = Word2Vec.load(word2vec_file_dir)
        vocab_size = len(word2vec.wv.vocab) + 1  # for unknown tokens
        print("Vocab Size: ", vocab_size)
        print("Loading Train Dataset")
        
        files=all_releases[project]
        train_files=files[:2]
        test_files=files[2:]
        
        train_dataset = BiLSTMDataset(word2vec, data_path, train_files,20,Train=True) 
        train_data_loader = DataLoader(train_dataset, batch_size=args.batch_size, num_workers=args.num_workers,pin_memory=True)
        
        
        test_dataset = BiLSTMDataset(word2vec, data_path, test_files,20,Train=False)
        test_data_loader = DataLoader(test_dataset, batch_size=args.batch_size, num_workers=args.num_workers,pin_memory=True)
        
        print("Building model")
        
        cuda_condiction = torch.cuda.is_available() and args.with_cuda
        device = torch.device("cuda:1" if cuda_condiction else "cpu")
        print(device)
        Model=Bilstm(500,64,2,device)
        
        print("Creating Trainer")
        trainer = Trainer(Model, args.alpha, train_dataloader=train_data_loader,test_dataloader=test_data_loader,
                            lr=args.lr, betas=(args.adam_beta1, args.adam_beta2), weight_decay=args.adam_weight_decay,
                            device=device, log_freq=args.log_freq)
        print("Training Start")
        
        with open(RQ_path+"lstm_result.txt","a") as f:
            f.write(project+"\n")
        for epoch in range(args.epochs):
            loss=trainer.train(epoch)
            
            if (epoch+1)%10==0:
                line_result=trainer.test(epoch)
                with open(RQ_path+"lstm_result.txt","a") as f:
                    try:
                        f.write(str(epoch+1)+" recall@20%LOC:"+str(line_result["recall@20%LOC"])
                        +" effort@20%Recall:"+str(line_result["effort@20%Recall"])+" auc: "+str(line_result["auc"])
                        +" balance_acc"+str(line_result["balance_acc"])+" mcc:"+str(line_result["mcc"])+" f1: "+str(line_result["f1"])
                        +" precision"+str(line_result["precision"])+" recall"+str(line_result["recall"])+" IFA"+str(line_result["IFA"])+"\n")
                    except:
                        f.write(str(epoch+1)+"\n")
        
        output_path=RQ_path+project
        trainer.save(epoch, output_path)
    f.close()

if __name__ == "__main__":
    train()