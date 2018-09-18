# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 11:00:04 2017

Random walk to generate a path streched on both directions.

@author: lil115
"""

import pandas as pd
import networkx as nx
import numpy as np
import itertools
import copy

WALK_TIME = 500
PATH_LEN = 20

def transform(di_li, pd_df):
    '''
    Take in dataframe and dictionary of lists version of the network.
    Output the initial data structure for random walk simulation.
    '''
    result = {}
    for start in di_li:
        target = di_li[start]
        result[start] = {'target': target}
        result[start]['weight'] = np.array([pd_df.loc[start,e] for e in target])
    return result
    


#current = np.random.choice(c.index,1,[1/len(c.index)]*len(c.index))

def random_walk(start,graph,PATH_LEN=PATH_LEN):
    '''
    Given walking steps, a graph and the starting node, this function returns random walk on both directions as a list.
    This random walk should not allow the node to walk back to the node right before it.
    If current node has a degree of 1. Random walk restart from the starting point.
    '''
    current = start
    seq = [current]
    current = np.random.choice(graph[current]['target'],1,p=graph[current]['weight']/sum(graph[current]['weight']))[0]
    seq.append(current)
    end = current
    start_t,start_d,end_t,end_d = graph[start]['target'], graph[start]['weight'], graph[end]['target'], graph[end]['weight']
    start_pos, end_pos = start_t.index(end), end_t.index(start)
    start_t, end_t = start_t[:start_pos] + start_t[(start_pos+1):], end_t[:end_pos] + end_t[(end_pos+1):]
    start_d, end_d = np.concatenate((start_d[:start_pos],start_d[(start_pos+1):])), np.concatenate((end_d[:end_pos],end_d[(end_pos+1):]))
    targets = start_t + end_t
    degree = np.concatenate((start_d,end_d))
    for i in range(PATH_LEN):
        #start_t,start_d,end_t,end_d = graph[start]['target'], graph[start]['weight'], graph[end]['target'], graph[end]['weight']
        if len(targets) == 0: break
        current = np.random.choice(targets,1,p=degree/sum(degree))[0]
        t = graph[current]
        if current in start_t:
            pos = t['target'].index(start)
            start = current
            start_t, start_d = t['target'][:pos]+t['target'][(pos+1):], np.concatenate((t['weight'][:pos],t['weight'][(pos+1):]))
            seq.insert(0,current)
        else:
            pos = t['target'].index(end)
            end = current
            end_t, end_d = t['target'][:pos]+t['target'][(pos+1):], np.concatenate((t['weight'][:pos],t['weight'][(pos+1):]))
            seq.append(current)
        targets = start_t + end_t
        degree = np.concatenate((start_d,end_d))
    return seq




g_ppi2 = nx.read_gpickle('D:/PPI-Topic/Processed_data/g_ppi_newdeg.csv')

di_ppi2 = nx.to_dict_of_lists(g_ppi2)
c_ppi2 = nx.to_pandas_dataframe(g_ppi2)      
seq = []
net_ppi2 = transform(di_ppi2,c_ppi2)
for node in g_ppi2.nodes():
    for i in range(WALK_TIME):
        seq.append(random_walk(node,net_ppi2) + ['#'])
    # print('node',node,'complete')
lexico = sorted(g_ppi2.nodes(), key=g_ppi2.degree, reverse=True)    
lexico1 = {e:lexico.index(e) for e in lexico}
lexico1['#'] = -1
seq_concat = list(itertools.chain.from_iterable(seq))
seq_int = [lexico1[e] for e in seq_concat]



