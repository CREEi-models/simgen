import numpy as np
import pandas as pd

class statistics:
    def __init__(self,stratas): 
        self.stratas = stratas
        self.counts = None
        return 
    def start(self,pop,year):
        counts = pop.hh.groupby(self.stratas).sum()['wgt']
        self.counts = pd.DataFrame({year:counts}).fillna(0.0)
        return
    def add(self,pop,year):
        counts = pop.hh.groupby(self.stratas).sum()['wgt']
        counts.name = year
        self.counts = self.counts.merge(counts,left_index=True,right_index=True,how='outer')
        self.counts = self.counts.fillna(0.0)
        return
    def freq(self,strata=None,bins=[0],sub=None):
        if sub!=None:
            counts = self.counts.query(sub)
        else :
            counts = self.counts.copy()
        if len(bins)<2:
            if strata!=None:
                df = pd.pivot_table(counts,index=strata,aggfunc=np.sum).transpose()
            else :
                df = counts.sum(axis=0)
            return df
        else :
            df = pd.pivot_table(counts,index=strata,aggfunc=np.sum)
            df = df.reset_index()
            df[strata] = pd.cut(df[strata],bins=bins)
            df = df.groupby(strata).sum().transpose()
            return df
    def prop(self,strata,bins=[0],sub=None):
        if sub!=None:
            counts = self.counts.query(sub)
        else :
            counts = self.counts.copy()
        if len(bins)<2:
            df = pd.pivot_table(counts,index=strata,aggfunc=np.sum).transpose()
            df = df.div(df.sum(axis=1),axis=0)
            return df 
        else :
            df = pd.pivot_table(counts,index=strata,aggfunc=np.sum)
            df = df.reset_index()
            df[strata] = pd.cut(df[strata],bins=bins)
            df = df.groupby(strata).sum().transpose()
            df = df.div(df.sum(axis=1),axis=0)
            return df





    


        
        