#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 19:23:29 2020

@author: loulou
"""
import pandas as pd
import numpy as np 
from random import choices
from functools import partial

npop = 1000000
doms = pd.DataFrame(index=np.arange(npop),columns=['wgt','byr','male','married','nkids'])
doms.index.name = 'nas'

doms['wgt'] = 1.0

doms['byr'] = np.floor(np.linspace(1940,2010,npop)).astype('Int32')     

doms['male'] = np.random.uniform(size=npop)<0.5

doms['married'] = np.random.uniform(size=npop)<0.8

ns = [0,1,2,3]
doms['nkids'] = choices(ns,k=npop)


nspouses = doms['married'].sum()

sps = pd.DataFrame(index=doms.index[doms.married],columns=['byr','male','active','wedyr','divyr'])
sps.index.name='nas'
byrs = np.arange(1950,2010)
sps['byr'] = choices(byrs,k=nspouses)

sps['active'] = True
sps['wedyr'] = sps['byr']+20

sps = sps.merge(doms['male'],left_index=True,right_index=True,suffixes=('','_dom'))
sps['male'] = sps['male_dom']!=True

nkids = doms['nkids'].sum()

kids = doms.loc[doms.index.repeat(doms.nkids)]
ages = [25,30,35]
kids['byr_k'] = kids['byr'] + choices(ages,k=len(kids)) 
kids = kids[['male','byr_k']]
kids.columns = ['male','byr']

# test on merging kids
doms.merge(kids,left_index=True,right_index=True,suffixes=('','_k'))

nimm = 1000
imm = pd.DataFrame(index=np.arange(nimm),columns=['wgt','byr','male','married','nkids'])
imm.index.name = 'nas'
def gennas(n,nnew):
    return np.arange(n+1,n+1+nnew)

imm.index = gennas(np.max(doms.index),nimm)
imm['wgt'] = 1
imm['byr'] = choices(np.arange(1950,2010),k=nimm)    

imm['male'] = np.random.uniform(size=nimm)<0.5

imm['married'] = np.random.uniform(size=nimm)<0.8

imm['nkids'] = choices(ns,k=nimm)


#doms = doms.append(imm)

kids['age'] = 2017 - kids.byr


check = doms.merge(kids.groupby('nas').min()['age'],left_index=True,right_index=True,how='left')



        
pop = population(doms,sps,kids)
newimm = population(imm)        
        

