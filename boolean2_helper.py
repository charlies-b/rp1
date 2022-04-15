#!/usr/bin/env python
# coding: utf-8

import warnings
warnings.filterwarnings("ignore")
import boolean2 as b2
import matplotlib as mpl
import matplotlib.pyplot as plt
import string_model_builder_3 as builder
from numpy.ma import masked_equal
import numpy as np
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable


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
    return model if runs==1 else models
    
def print_model(model): # print node states
    for node in model.data:
        print node, model.data[node]
        
def average_models(models, nodes = None, w=10, h=32): # average array of models (from booleannet docs)
    coll = b2.util.Collector()
    for model in models:
        coll.collect(states = model.states, nodes=model.nodes)
    avgs = coll.get_averages()     
    return avgs

def get_cycles(models):
    # (start index, size) 
    # size = 0 => no cycle/steady state
    # size = 1 => steady state
    return [ model.detect_cycles() for model in models]

def count_cycles(cycles):
    # (# none, # steady, # other)
    none = 0
    steady = 0
    other = 0 
    for cycle in cycles:
        if cycle[1] == 0: none+=1
        elif cycle[1] == 1: steady+=1
        else: other+=1
    return ('none: '+str(none), 'steady: '+str(steady), 'other: '+str(other))

def print_cycles(cycles):
    print "index", '\t', 'size'
    for cycle in cycles: 
        print cycle[0], '\t', cycle[1]   

def average_cycles(cycles):
    return np.average(cycles, 0)
        


def plot_data(data, ax,
              nodes=None,
              title = None
             ): # plots model.data (node states) onto axis

    # select plot data
    plot = []
    labels = sorted(data.keys()) if not nodes else nodes # sort alphabetically, or a list of ordered nodes
    for label in labels:
        bindata = np.array(data[label]).astype(float) # convert bool to bin if necessary
        plot.append(bindata)
        
    # plot data
    cmap=mpl.cm.gray # off (0) = black, on (1) = white
    norm = mpl.colors.Normalize(vmin=0, vmax=1) # make sure 0 is always mapped to white, 1 to black
    im = ax.imshow(plot, cmap=cmap, norm=norm)
    ax.set_yticks(np.arange(len(labels)))
    ax.set_yticklabels(labels)
    ax.set_aspect('auto')
    if title: ax.set_title(title)
    ax.set_xlabel('steps')
    return im # return handle to the axes for stupid colour bar

def plot_maps(datas, # array of model.data 
              titles = [], # map titles in same order
              nodes = [],  # nodes plotted across all maps
              filename='map.png', 
              suptitle='    Average Node State Heatmap', 
              fontsize=16,
              suptitlesize = 24,
              h = 18, # inches
              w = 20, # inches
              left = 0.2,  # the left side of the subplots of the figure
              right = 0.9,   # the right side of the subplots of the figure
              bottom = 0.1,  # the bottom of the subplots of the figure
              top = 0.95,     # the top of the subplots of the figure
              wspace = 0.2,  # the amount of width reserved for space between subplots
              hspace = 0.2,  # the amount of height reserved for space between subplots
              dpi = 200
             ): # sets up axes into subplot
    plt.rcParams.update({'font.size': fontsize})
    
    # setup plot
    fig, axes = plt.subplots(len(datas),1, figsize=(w,len(datas)*h))#, figsize=(10,2))
    axes = axes if not len(datas)==1 else [axes]    # plot axes
   
    if not titles: titles = range(1, len(datas)+1)
    for data, ax, title in zip(datas, axes , titles ):
        if not nodes: nodes = sorted(data.keys())
        im = plot_data(data, ax, nodes = nodes, title=title)   
        # add colour bar
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='2%', pad='1%')
        fig.colorbar(im, orientation = 'vertical', cax= cax)
        
    # adjust
    plt.subplots_adjust(hspace=hspace, top=top, left=left, right=right, wspace=wspace, bottom=bottom)
    fig.suptitle(suptitle, fontsize = suptitlesize)
    
    # show savedown
    plt.show()
    fig.savefig(filename, dpi=dpi)
        
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
      