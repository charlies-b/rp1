#!/usr/bin/env python
# coding: utf-8

import warnings
warnings.filterwarnings("ignore")
import boolean2 as b2
import matplotlib.pyplot as plt
from numpy.ma import masked_equal
from matplotlib.colors import ListedColormap

def missing( node_name ): # initialise any loose nodes True
    return True

def run_model(definition, runs=1, steps=15, mode='sync'): # returns array of models of length runs  
    models = []
    for i in range(runs):
        # run model under settings
        model = b2.Model(text=definition, mode=mode)
        model.initialize( missing=missing ) # initialise any loose nodes to true
        model.iterate(steps=steps)
        models.append(model)
    return models
    
def print_model(model): # print node states
    for node in model.data:
        print node, model.data[node]
        
def plot_model(model, nodes=None, w=10, h=32): # plot node states    
    # get data from model
    data = []
    labels = sorted(model.data.keys()) if not nodes else nodes # sort alphabetically, or a list of ordered nodes
    for label in labels:
        data.append(model.data[label])
        
    # plot figure
    cmap=plt.cm.get_cmap('gray') # off (0) = black, on (1) = white
    plt.yticks(range(0, len(labels)), labels)
    plt.imshow(data, cmap=cmap)
    plt.gcf().set_size_inches(w, h)

class DummyModel: # dummy model with data attribute
    def __init__(self, data):
        self.data = data
        
def plot_average(models, nodes = None, w=10, h=32):
    # collect models into average (from booleannet docs)
    coll = b2.util.Collector()
    for model in models:
        coll.collect(states = model.states, nodes=model.nodes)
    avgs = coll.get_averages()   
    
    # plot average model
    avg_model = DummyModel(avgs) # so it can be passed to plot_model plain
    plot_model(avg_model, nodes=nodes, w=w, h=h)

def knockout(definition, knockouts=[]):
    assert isinstance(knockouts, list), "takes list"
    new_definition = definition.split('\n')
    for knockout in knockouts:
        for i, line in enumerate(new_definition):
            if line.startswith(knockout):
                new_definition[i] = '#'+line # comment initialisation and rule
                continue
        new_definition.insert(1,knockout + ' = False #knockout') # make off
    return '\n'.join(new_definition)
        
def switch(definition, on=[], off=[]):
    assert isinstance(on, list), "takes list"
    assert isinstance(off, list), "takes list"
    
    new_definition = definition.split('\n')
    for node in on+off:
        for i, line in enumerate(new_definition):
            if line.startswith(node + ' ='): # initialisation NOT rule '*='
                if node in on and node not in off:
                    new_definition[i] = node +' = True' # switch on
                if node in off and node not in on:
                    new_definition[i] = node +' = False' # switch off
                continue
    return '\n'.join(new_definition)
      