#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 10:02:44 2020

@author: loulou
"""
import numpy 
import pandas as pd

class distage:
    def __init__(self,ngap=1):
        return
    def counts(self,pop,year):
        data = [[p.age(year),p.wgt] for p in pop]
        df = pd.DataFrame(data=data,columns=['age','wgt'])
        result = df.groupby('age').sum()
        return result
        
        