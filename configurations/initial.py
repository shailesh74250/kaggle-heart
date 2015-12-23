#TODO: add code
from default import *

import theano.tensor as T
import objectives


def build_model():
    l0 = lasagne.layers.InputLayer((batch_size, 1, 255, 255))
    l0s = lasagne.layers.cuda_convnet.bc01_to_c01b(l0)

    l1a = lasagne.layers.cuda_convnet.Conv2DCCLayer(l0s, num_filters=32, filter_size=(3, 3), pad="same",
                                               b=lasagne.init.Constant(0.1), dimshuffle=False)
    l1b = lasagne.layers.cuda_convnet.Conv2DCCLayer(l1a, num_filters=32, filter_size=(3, 3), pad="same",
                                               b=lasagne.init.Constant(0.1), dimshuffle=False)

    l2a = lasagne.layers.cuda_convnet.Conv2DCCLayer(l1b, num_filters=64, filter_size=(3, 3), pad="same",
                                               b=lasagne.init.Constant(0.1), dimshuffle=False)
    l2b = lasagne.layers.cuda_convnet.Conv2DCCLayer(l2a, num_filters=64, filter_size=(3, 3), pad="same",
                                               b=lasagne.init.Constant(0.1), dimshuffle=False)

    l3a = lasagne.layers.cuda_convnet.Conv2DCCLayer(l2b, num_filters=128, filter_size=(3, 3), pad="same",
                                               b=lasagne.init.Constant(0.1), dimshuffle=False)
    l3b = lasagne.layers.cuda_convnet.Conv2DCCLayer(l3a, num_filters=128, filter_size=(3, 3), pad="same",
                                               b=lasagne.init.Constant(0.1), dimshuffle=False)

    l4a = lasagne.layers.cuda_convnet.Conv2DCCLayer(l3b, num_filters=128, filter_size=(3, 3), pad="same",
                                               b=lasagne.init.Constant(0.1), dimshuffle=False)
    l4b = lasagne.layers.cuda_convnet.Conv2DCCLayer(l4a, num_filters=128, filter_size=(3, 3), pad="same",
                                               b=lasagne.init.Constant(0.1), dimshuffle=False)
    l4s = lasagne.layers.cuda_convnet.c01b_to_bc01(l4b)
    l5 = lasagne.layers.DenseLayer(lasagne.layers.dropout(l4s, p=0.5), num_units=128, b=lasagne.init.Constant(0.1))

    l6 = lasagne.layers.DenseLayer(lasagne.layers.dropout(l5, p=0.5), num_units=128, b=lasagne.init.Constant(0.1))

    l7 = lasagne.layers.DenseLayer(lasagne.layers.dropout(l6, p=0.5), num_units=256*256, nonlinearity=T.nnet.ultra_fast_sigmoid)

    return {
        "inputs":[l0],
        "output":l7
    }

def build_objective(l_ins, l_out):
    return objectives.BinaryCrossentropyImageObjective(l_out)