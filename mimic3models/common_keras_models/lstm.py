from keras import backend as K
from keras.models import Model
from keras.layers import Input, Dense, LSTM, Masking, Dropout
from keras.layers.wrappers import Bidirectional

class Network(Model):
    
    def __init__(self, dim, batch_norm, dropout, task, num_classes=1,
                depth=0, input_dim=76, **kwargs):
        
        print "==> not used params in network class:", kwargs.keys()
        
        # TODO: dropout and batch_norm
        
        self.dim = dim
        self.batch_norm = batch_norm
        self.dropout = dropout
        self.depth = depth
        
        if task in ['decomp', 'ihm', 'ph']:
            final_activation = 'sigmoid'
        elif task in ['los']:
            if num_classes == 1:
                final_activation = 'relu' # TODO: what if it is regression but in log-space
            else:
                final_activation = 'softmax'
        else:
            return ValueError("Wrong value for task")
        
        
        X = Input(shape=(None, input_dim), name='X')
        mX = Masking()(X)
        
        for i in range(depth):
            mX = Bidirectional(LSTM(units=dim//(2**i),
                                   activation='tanh',
                                   return_sequences=True,
                                   dropout=dropout))(mX)

        L = LSTM(units=dim,
                 activation='tanh',
                 return_sequences=False,
                 dropout=dropout)(mX)
        
        y = Dense(num_classes, activation=final_activation)(L)
        
        return super(Network, self).__init__(inputs=[X],
                                             outputs=[y])
    
    
    def say_name(self):
        self.network_class_name = "k_lstm"
        return "{}.n{}{}{}.dep{}".format(self.network_class_name,
                                 self.dim,
                                 ".bn" if self.batch_norm else "",
                                 ".d{}".format(self.dropout) if self.dropout > 0 else "",
                                 self.depth)