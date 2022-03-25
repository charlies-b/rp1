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

def run_model(definition, steps=15, mode='sync'): # run model under settings
    model = b2.Model(text=definition, mode=mode)
    model.initialize( missing=missing ) # initialise any loose nodes
    model.iterate(steps=steps)
    return model
    
def print_model(model): # print node states
    for node in model.data:
        print node, model.data[node]

cmap = ListedColormap(['green'])
cmap.set_bad('red')

def plot_model(model, w=10, h=32): # plot node states 
    data = []
    labels = sorted(model.data.keys()) # nodes sorted alphabetically
    for label in labels:
        data.append(model.data[label])
        
    # figure
    plt.yticks(range(0, len(labels)), labels)
    plt.imshow(masked_equal(data, 0), cmap= cmap)
    plt.gcf().set_size_inches(w, h)
    plt.show()

def plot_nodes(model, nodes, w=10, h=32): # plot node states 
    data = []
    labels = nodes 
    for label in labels:
        data.append(model.data[label])
        
    # figure
    plt.yticks(range(0, len(labels)), labels)
    plt.imshow(masked_equal(data, 0), cmap= cmap)
    plt.gcf().set_size_inches(w, h)
    plt.show()

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
      