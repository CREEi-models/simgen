import numpy as np 
import pandas as pd


class parse:
    def __init__(self):
        self.vars_hh = ['wgt','byr','male','educ','insch','nkids','married']
        self.map_hh = dict(zip(self.vars_hh,self.vars_hh))
        self.vars_sp = ['byr','male','educ','insch']
        self.map_sp = dict(zip(self.vars_sp,self.vars_sp))
        self.vars_kd = ['byr','male','insch']
        self.map_kd = dict(zip(self.vars_kd,self.vars_kd))
        return
    def dominants(self,data):
        hh = pd.DataFrame(index=data.index,columns=self.vars_hh)
        for m in self.vars_hh:
            if self.map_hh[m] in data.columns:
                hh[m] = data[self.map_hh[m]]
        hh.index.name = 'nas'
        self.hh = hh
        hh.wgt = hh.wgt.astype('Float64')
        hh.nkids = hh.nkids.astype('Int64')
        return hh
    def spouses(self,data):
        n = len(data)
        if n==len(self.hh.index[self.hh.married]):
            sp = pd.DataFrame(index=data.index,columns=self.vars_sp)
            for m in self.vars_sp:
                if self.map_sp[m] in data.columns:
                    sp[m] = data[self.map_sp[m]]
            sp.index.name = 'nas'
            self.sp = sp
            return sp
        else :
            print('number of spouses in data not equal to number of dominants married')
            return None
    def kids(self,data):
        n = len(data)
        if n==self.hh['nkids'].sum():
            kd = pd.DataFrame(index=data.index,columns=self.vars_kd)
            for m in self.vars_kd:
                if self.map_kd[m] in data.columns:
                    kd[m] = data[self.map_kd[m]]
            kd.index.name = 'nas'
            self.kd = kd
            return kd
        else :
            print('number of kids in data not equal to total number of kids in dominant')
            return None


class population:
    def __init__(self,hh,sp,kd):
        self.hh = hh
        self.sp = sp
        self.kd = kd
        return
    def size(self,w=True):
        if w:
            return self.hh['wgt'].sum()
        else:
            return len(self.hh)
    def gennas(self,n):
        maxnas = self.hh.index.max()
        return np.arange(maxnas+1,maxnas+1+n)
    def enter(self,imm,ntarget):
        nimm = len(imm.hh)
        nwgt = imm.hh.wgt.sum()
        imm.hh.wgt = imm.hh.wgt * ntarget/nwgt
        # generate new nas and assign
        new_nas = self.gennas(nimm)
        assign = dict(zip(imm.hh.index.values,new_nas))
        imm.hh.index = imm.hh.index.to_series().replace(assign)
        self.hh = self.hh.append(imm.hh)
        imm.sp.index = imm.sp.index.to_series().replace(assign)
        self.sp = self.sp.append(imm.sp)
        imm.kd.index = imm.kd.index.to_series().replace(assign)
        self.kd = self.kd.append(imm.kd)
        return 
    def exit(self,nastodrop):
        self.hh = self.hh.drop(nastodrop,errors='ignore')
        self.sp = self.sp.drop(nastodrop,errors='ignore')
        self.kd = self.kd.drop(nastodrop,errors='ignore')
        return
    def merge_spouses(self):
        return self.hh.merge(self.sp,left_index=True,right_index=True,
                             how='left',suffixes=('','_sp'))
    def nkids(self):
        nk = self.kd.groupby('nas').count()['byr']
        nk.name = 'nkids'
        self.hh.loc[nk.index,'nkids'] = nk
        self.hh.loc[~self.hh.index.isin(nk.index),'nkids'] = 0
        return 
    def ages(self,year):
        self.hh['age'] = year - self.hh['byr']
        self.sp['age'] = year - self.sp['byr']
        self.kd['age'] = year - self.kd['byr']
        return        
    def kagemin(self):
        am = self.kd.groupby('nas').min()['age']
        am.name = 'agemin'
        if 'agemin' in self.hh.columns:
            self.hh.loc[am.index,'agemin'] = am
            self.hh.loc[~self.hh.index.isin(am.index),'agemin'] = 0
        else :
            self.hh['agemin'] = 0
            self.hh.loc[am.index,'agemin'] = am
        return    
        
                
        