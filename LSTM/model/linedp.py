import torch
import torch.nn as nn
from model.transformer import MultiHeadAttentionLayer


class LineDP(nn.Module):
    def __init__(self, transformer, target):
        super(LineDP, self).__init__()
        self.transformer=transformer
        # for parameter in self.parameters():
        #     parameter.requires_grad=False
        self.DP = DP(self.transformer.hidden, 12, target, dropout=0.1)


    def forward(self, x, p, y):
        output = self.transformer(x, p, y)
        target, attention = self.DP(output)
        return target, attention


class DP(nn.Module):
    def __init__(self, hidden, n_head, target, dropout):
        super(DP, self).__init__()
        self.attention = MultiHeadAttentionLayer(hidden, n_head, dropout)
        self.target_predict = nn.Linear(hidden, target)
        self.softmax=nn.LogSoftmax(dim=-1)
        self.sig = nn.Sigmoid()

    def forward(self, src):
        src, attention = self.attention(src, src, src)
        target = self.target_predict(src[:, -2:-1, :]).squeeze(1)
        token_attention=self.softmax(src[:,1:-2,:])
        return self.sig(target), attention