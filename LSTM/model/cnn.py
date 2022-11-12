import math
import os
import torch
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader, TensorDataset
import torch.autograd as autograd
import torch.nn as nn
import torch.nn.functional as F

class TextCNN(nn.Module):
    def __init__(self, vocab_size, embed_size,feature_size,window_sizes=[3,4,5,6],max_text_len=22,dropput_rate=0.5):
        super(TextCNN, self).__init__()
        
        self.vocab_size=vocab_size
        self.embed_size=embed_size
        self.feature_size=feature_size
        self.window_sizes=window_sizes
        self.max_text_len=max_text_len
        self.dropout_rate=dropput_rate
 
        self.embedding = nn.Embedding(self.vocab_size,self.embed_size)
        self.convs = nn.ModuleList([
                nn.Sequential(nn.Conv1d(in_channels=self.embed_size, 
                                        out_channels=self.feature_size, 
                                        kernel_size=h),
#                              nn.BatchNorm1d(num_features=config.feature_size), 
                              nn.ReLU(),
                              nn.MaxPool1d(kernel_size=self.max_text_len-h+1))
                     for h in self.window_sizes
                    ])
        self.fc = nn.Linear(in_features=self.feature_size*len(self.window_sizes),
                            out_features=1)
        self.sigmoid = nn.Sigmoid()
        self.dropout = nn.Dropout(0.5)
        
    def forward(self, x):
        embed_x = self.embedding(x)
        
        #print('embed size 1',embed_x.size())  # 32*35*256
        # batch_size x text_len x embedding_size  -> batch_size x embedding_size x text_len
        embed_x = embed_x.permute(0, 2, 1)
        #print('embed size 2',embed_x.size())  # 32*256*35
        out = [conv(embed_x) for conv in self.convs]  #out[i]:batch_size x feature_size*1
        #for o in out:
        #    print('o',o.size())  # 32*100*1
        out = torch.cat(out, dim=1)  # 对应第二个维度（行）拼接起来，比如说5*2*1,5*3*1的拼接变成5*5*1
        #print(out.size(1)) # 32*400*1
        out = out.view(-1, out.size(1)) 
        #print(out.size())  # 32*400 
        # if not self.use_element:
        out = F.dropout(input=out, p=self.dropout_rate)
        out = self.fc(out)
        out=self.sigmoid(out)
        return out