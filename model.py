import torch.nn as nn
import torch
import numpy as np


class baselineGRU(nn.Module):
    def __init__(self):
        super(baselineGRU, self).__init__()
        self.input_dim = 208
        self.hidden_dim = 100
        self.output_dim = 98
        self.batch_size = 2
        self.num_layers = 2
        self.dropout = 0.2
        self.bidirect = False
        self.cuda = False

        # input layer requried?
        self.gru = nn.GRU(self.input_dim, self.hidden_dim, self.num_layers,
                          bias=True, dropout=self.dropout,
                          bidirectional=self.bidirect, batch_first=True)

        directions = 2 if self.bidirect else 1
        self.out = nn.Linear(self.hidden_dim * directions, self.output_dim)
        if (self.cuda):
            self.gru, self.out = self.gru.cuda(), self.out.cuda()

        # load model cache
        self.load_state_dict(torch.load("./model_cache", map_location='cpu'))

    def init_hidden(self, batch_size):
        # Before we've done anything, we dont have any hidden state.
        # Refer to the Pytorch documentation to see exactly
        # why they have this dimensionality.
        # The axes semantics are (num_layers, minibatch_size, hidden_dim)
        directions = 2 if self.bidirect else 1
        return torch.zeros(self.num_layers * directions, batch_size,
                           self.hidden_dim)

    def forward(self, sequence):
        '''
        Takes in the sequence of the form
        (batch_size x sequence_length x input_dim) and
        returns the output of form
        (batch_size x sequence_length x output_dim)
        '''

        if (self.cuda):
            if (type(sequence).__module__ == np.__name__):
                sequence = torch.Tensor(sequence).cuda()
            else:
                sequence = sequence.cuda()
            if isinstance(self.hidden, tuple):
                self.hidden = (self.hidden[0].cuda(), self.hidden[1].cuda())
            else:
                self.hidden = self.hidden.cuda()

        output, self.hidden = self.gru(sequence, self.hidden)
        del sequence
        output = self.out(output)
        return output
