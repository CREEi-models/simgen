#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# import basic libraries
import numpy as np 
from matplotlib import pyplot as plt
import pandas as pd
from importlib import reload
from copy import deepcopy
import warnings
warnings.filterwarnings("ignore")
# load tools
import sys
sys.path.append('/users/loulou/cedia/OLG_CAN/demo/compas/')

from compas import bdsps, population, parse, update, isq

# reload libraries 


# main population
hh,sp,kd = bdsps('../raw/bdsps2017.dta')

# new immigrants
imm = hh[hh.newimm]
imm_nas = imm.index
sp_imm = sp.loc[sp.index.isin(imm_nas),:]
kd_imm = kd.loc[kd.index.isin(imm_nas),:]

# parsing for variable names
parsing = parse()
parsing.map_hh['educ'] = 'educ4'
parsing.map_hh['insch'] = 'inschool'
parsing.map_sp['educ'] = 'educ4'
parsing.map_sp['insch'] = 'inschool'
parsing.map_kd['insch'] = 'inschool'

# parsing to create correct variable names
hh = parsing.dominants(hh)
sp = parsing.spouses(sp)
kd = parsing.kids(kd)

# parsing to create correct variable names
imm = parsing.dominants(imm)
sp_imm = parsing.spouses(sp_imm)
kd_imm = parsing.kids(kd_imm)

# encapsulating into a population structure
pop = population()
pop.input(hh,sp,kd)
pop.save('startpop')

pop.load('startpop')

newimm = population()
newimm.input(imm,sp_imm,kd_imm)
newimm.save('newimmpop')

trans = update()

isq = pd.read_excel('../raw/isq/naissance_ed2019.xlsx',sheet_name='rates')
isq = isq.set_index('year')


plt.figure()
for a in range(2017,2040):
    pop = trans.divorce(pop,a)
    pop = trans.marriage(pop,a)
    if a!=2017:
        pop = trans.birth(pop,a,isq.loc[a,'reference']*pop.size())
    pop = trans.dead(pop,a)
    pop = trans.kids_dead(pop,a)
    pop = trans.sp_dead(pop,a)
    pop = trans.moveout(pop,a)
    newimm.hh.byr += 1
    newimm.sp.byr += 1
    newimm.kd.byr += 1
    pop.enter(newimm,0.005*pop.size())
    print(a,pop.size())
    age = pop.hh.groupby('age').sum()['wgt']
    plt.plot(age.index,age,label=str(a))
plt.show()


# create an instance of model
simul = demographics.dynamics
qc = simul()

# create instance of statistics
sage = statistics.distage()

# set assumptions
qc.immig_assumptions(rate=50e3/8.3e6,init=[deepcopy(p) for p in initnewimm])
qc.babies_assumptions(scenario='reference',align=True)
qc.dead_assumptions(scenario='medium')
# perform simulation
pop = [deepcopy(p) for p in initpop]
year = 2017
plt.figure()
for i in range(10):
    newpop = qc.oneyear(pop,year)
    for p in newpop:
        if p.age(year)<0:
            print(p.nas,p.byear,p.male,p.educ,p.nkids(),p.agekids(year))
    #print(i,' *** change in pop: ',len(newpop)-len(pop))
    #print(np.mean([p.sp!=None for p in newpop]))
    popage = sage.counts(newpop,year).reset_index()
    print(popage)
    plt.plot(popage['age'],popage['wgt'],label=str(year))
    print('pop size = ',year,popage['wgt'].sum())
    pop = newpop[:]
    year +=1
plt.legend()
plt.show()