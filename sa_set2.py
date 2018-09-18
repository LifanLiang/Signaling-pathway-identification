#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 12:39:47 2017

@author: lifan
"""

import itertools
#import pandas as pd


def sa_set2(seq):
    '''
    Constructing suffix arrays using set2 algorithm.
    '''
    maxn = max(seq)
    length = len(seq)
    seq.append(-1)
    k = 4
    
    suffix = [{0:ind, 1:seq[ind], 2:seq[ind+1]} for ind in range(len(seq)-1)]
    while(k < (2*length)):
        #print(suffix)
        suffix = radix_sort(suffix,maxn)
        suffix,unique = update_index(suffix,k)
        if unique: break
        k *= 2
        maxn = suffix[-1][1]
    return [e[0] for e in suffix]
           
def radix_sort(tri12_int,maxn):
    '''
    Given a list of integer tuples. This algorithm sorted a list of tuples and return a suffix array.
    '''
    sorted_tri = tri12_int
    for i in range(2,0,-1):
        buckets = [[] for e in range(maxn+2)]
        # Special symbol '-1' would be added in the end.
        for e in sorted_tri:
            buckets[e[i]].append(e)
        buckets.insert(0,buckets[-1])
        del buckets[-1]
        sorted_tri = list(itertools.chain.from_iterable(buckets))
    return sorted_tri

def update_index(suffix,k):
    '''
    Update the first rank and the second rank in the sorted index.
    '''
    n = len(suffix)
    unique = True
    prev_rank = suffix[0][1]
    rank = 0
    for i in range(1,n):
        if suffix[i][1] == prev_rank and suffix[i][2] == suffix[i-1][2]:
            prev_rank = suffix[i][1]
            suffix[i][1] = rank
            unique = False
        else:
            prev_rank = suffix[i][1]
            rank += 1
            suffix[i][1] = rank
    inv_ind = [0] * n
    for i in range(n):
        inv_ind[suffix[i][0]] = i
    for i in range(n):
        j = int(suffix[i][0] + k/2)
        suffix[i][2] = suffix[inv_ind[j]][1] if j < n else -1
    return suffix, unique
    
    
assert sa_set2([1,0,2,0,2,0]) == [5,3,1,0,4,2]
assert sa_set2([1,0,3,3,0,3,3,0,2,2,0]) == [10,7,4,1,0,9,8,6,3,5,2]
radix_sort([{0: 0, 1: 1, 2: 0}, {0: 1, 1: 0, 2: 2}, {0: 2, 1: 2, 2: 0}, {0: 3, 1: 0, 2: 2}, {0: 4, 1: 2, 2: 0}, {0: 5, 1: 0, 2: -1}],2)
update_index([{0: 5, 1: 0, 2: -1}, {0: 1, 1: 0, 2: 2}, {0: 3, 1: 0, 2: 2}, {0: 0, 1: 1, 2: 0}, {0: 2, 1: 2, 2: 0}, {0: 4, 1: 2, 2: 0}],4)
