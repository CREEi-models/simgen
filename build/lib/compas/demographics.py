from tools.actors import person, spouse, kid  
import numpy as np 
from numba import njit 
from multiprocessing import Pool as pool
from multiprocessing import cpu_count
from functools import partial
from tools import transition
import pandas as pd
from copy import deepcopy
from random import choices

class dynamics:
    def __init__(self,start_yr=2017,stop_yr=2100):
        self.start_yr = start_yr
        self.stop_yr = stop_yr
        self.trans = transition.update()
        return
    def immig_assumptions(self,rate=0.0,init=None):
        self.immig_rate = rate
        self.imm = init
    def babies_assumptions(self,scenario='reference',align=True):
        isq = pd.read_excel('../raw/isq/naissance_ed2019.xlsx',sheet_name='rates')
        isq = isq.set_index('year')
        maxyr = isq.index.max()
        if maxyr<self.stop_yr:
            for i in range(maxyr+1,self.stop_yr+1):
                isq.loc[i,:] = isq.loc[maxyr,:]
        self.align_babies = align
        self.adjust_babies = isq[scenario]
    def dead_assumptions(self,scenario='medium',improve=True):
        df = pd.read_csv('../params/trans_mortality_'+scenario+'.csv',sep=';')
        columns = ['year','male','prov']
        for a in range(0,111):
            columns.append(a)
        df.columns = columns
        df = df.drop(columns=['prov'])
        df['male'] = df['male'].replace({1:True,0:False})
        df = df.set_index(['year','male'])
        self.trans.params_dead(df,improve)
        return
    def move(self,p,year):
        # education
        p = self.trans.school(p,year)
        # divorces 
        p = self.trans.divorce(p,year)
        # new unions
        p = self.trans.marriage(p,year)
        # births
        if year!=self.start_yr:
            p = self.trans.birth(p,year)
        # spouse dies
        p = self.trans.sp_dead(p,year)
        # kids die
        p = self.trans.kids_dead(p,year)
        # kids move out
        p = self.trans.moveout(p,year) 
        # death at end of year
        p = self.trans.dead(p,year)
        # emigrates at end of year
        if p!=None: 
            p = self.trans.emig(p,year) 
        return p     
    def oneyear(self,pop,year):
        # transition
        if len(pop)>0:
            next_pop = []
            npop = np.sum([p.wgt for p in pop])
            print('size before transition',len(pop))
            p = pool(cpu_count())
            f = partial(self.move,year=year)
            next_pop = p.map(f,pop)
            p.close()
            print('size after transition',len(next_pop))            
            # clean up dead and emigrating households
            next_pop = [p for p in next_pop if p!=None]
            print('size after dropping dead',len(next_pop))
            # newborns
            babies = [p.wgt for p in next_pop if p.newborn(year)]
            nbabies = len(babies)
            if self.align_babies:    
                sim_babies = np.sum(babies)
                isq_babies = self.adjust_babies[year]*npop
                babies = [w*isq_babies/sim_babies for w in babies]
            if year!=self.start_yr:
                for b in range(nbabies):
                    next_pop.append(person(b=year,w=babies[b],male=np.random.uniform()<=0.5,e='none'))
            print('size after adding babies',len(next_pop))    
            # immigration 
            imm = [deepcopy(p) for p in self.imm]
            if self.immig_rate!=0.0:
                nimm = int(self.immig_rate*npop)
                nwgt = np.sum([i.wgt for i in imm])
                imm = choices(imm,k=len(imm))
                for i in imm:
                    i.nas = 1
                    i.wgt = i.wgt*nimm/nwgt
                    i.byear = i.byear + (year - self.start_yr)
                    if i.byear > year:
                        print('weird case among adult',i.nas,i.byear)
                    for k in i.kids:
                        k.byear = k.byear + (year - self.start_yr)
                        if k.byear>year:
                            print('weird case among kid')
                    next_pop.append(i)
            print('size after adding immigrants',len(next_pop)) 
        return next_pop