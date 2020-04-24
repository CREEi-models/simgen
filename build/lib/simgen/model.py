import numpy as np 
from numba import njit 
from multiprocessing import Pool as pool
from multiprocessing import cpu_count
from functools import partial
from simgen import update, population, statistics
import pandas as pd
from copy import deepcopy
from random import choices
from os import path
params_dir = path.join(path.dirname(__file__), 'params/')

class model:
    """ 
    Modèle de simulation SimGen.

    Cette classe permet de créer une instance d'un modèle de microsimulation.

    Parameters
    ----------
    start_yr : int 
        starting year of simulation
    stop_yr : int
        last year of simulation
    """
    def __init__(self,start_yr=2017,stop_yr=2100):
        self.start_yr = start_yr
        self.stop_yr = stop_yr
        self.year = start_yr
        self.trans = update()
        self.set_statistics()
        return
    def startpop(self,file):
        """
        Charger une population de départ.

        Fonction membre qui permet de charger une population de départ. 

        Parameters
        ----------
        file : str
            nom du fichier contenant la population de départ
        """
        self.ipop = population()
        self.ipop = self.ipop.load(file)
        return
    def immig_assumptions(self,allow=True,rate=0.0053478,init=None):
        """
        Hypothèses d'immigration.

        Fonction membre qui permet de spécifier les hypothèses d'immigration.

        Parameters
        ----------
        allow : boolean
            switch pour aligner le nombre d'immigrants sur ISQ
        rate : float
            taux d'immigration (par 100 personne). Par défaut, scénario de référence de l'ISQ. 
        init : str 
            nom du fichier contenant la population d'immigrants
        """
        # the 0.005 rate is from Statcan
        self.immig_allow = allow
        if allow:
            self.immig_rate = rate
            # this should be a population structure with new immigrants
            self.imm = population()
            self.imm = self.imm.load(init)
        else :
            self.immig_rate = 0.0 
            self.imm = None
        return
    def birth_assumptions(self,scenario='reference',align=True):
        isq = pd.read_excel(params_dir+'naissance_ed2019.xlsx',sheet_name='rates')
        isq = isq.set_index('year')
        maxyr = isq.index.max()
        if maxyr<self.stop_yr:
            for i in range(maxyr+1,self.stop_yr+1):
                isq.loc[i,:] = isq.loc[maxyr,:]
        self.align_births = align
        self.adjust_births = isq[scenario]
        return 
    def dead_assumptions(self,scenario='medium'):
        self.trans.params_dead(scenario)
        return
    def set_statistics(self,stratas=['age','male','educ','married','nkids']):
        self.stats = statistics(stratas)
        return
    def reset(self):
        self.pop = deepcopy(self.ipop)
        self.year = self.start_yr
        self.pop.ages(self.year)
        self.pop.nkids()
        self.pop.kagemin()
        self.stats.start(self.pop,self.year)
        return 
    def next(self):
        self.year +=1
        if len(self.pop.hh)>0:
            pop = self.pop
            yr = self.year
            trans = self.trans
            pop = trans.educ(pop,yr)
            pop = trans.divorce(pop,yr)
            pop = trans.marriage(pop,yr)
            if yr>self.start_yr:
                pop = trans.birth(pop,yr,self.adjust_births[yr]*pop.size())
            pop = trans.dead(pop,yr)
            pop = trans.kids_dead(pop,yr)
            pop = trans.sp_dead(pop,yr)
            pop = trans.moveout(pop,yr)
            pop = trans.emig(pop,yr)
            if self.immig_allow:
                newimm = deepcopy(self.imm) 
                newimm.hh.byr += (yr - self.start_yr)
                newimm.sp.byr += (yr - self.start_yr)
                newimm.kd.byr += (yr - self.start_yr)
                pop.enter(newimm,self.immig_rate*pop.size())
                pop.ages(yr)
                pop.nkids()
                pop.kagemin()
            self.pop = pop
        return 
    def simulate(self):
        self.reset()
        self.stats.start(self.pop,self.year)
        while self.year <= self.stop_yr:
            print(self.year,end='\r')
            self.next()
            self.stats.add(self.pop,self.year)
        return 