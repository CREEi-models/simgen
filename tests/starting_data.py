"""
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
sys.path.append('/Users/ydecarie/Dropbox (CEDIA)/simgem/simgen/simgen')

import data

# reload libraries 


# main population

hh,sp,kd = data.bdsps('/Users/ydecarie/Dropbox (CEDIA)/simgem/simgen/raw/bdsps2017.dta')

# new immigrants
imm = hh[hh.newimm]
imm_nas = imm.index
sp_imm = sp.loc[sp.index.isin(imm_nas),:]
kd_imm = kd.loc[kd.index.isin(imm_nas),:]

# parsing for variable names
parsing = data.parse()
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
pop = data.population()
pop.input(hh,sp,kd)
pop.save('/Users/ydecarie/Dropbox (CEDIA)/simgem/simgen/tests/startpopiso')

pop = data.population()
pop.load('/Users/ydecarie/Dropbox (CEDIA)/simgem/simgen/tests/startpopiso')

newimm = data.population()
newimm.input(imm,sp_imm,kd_imm)
newimm.save('/Users/ydecarie/Dropbox (CEDIA)/simgem/simgen/tests/newimmpopiso')
"""
import sys
import warnings
import pandas as pd 
import numpy as np
from matplotlib import pyplot as plt
warnings.filterwarnings("ignore")

sys.path.append('/Users/ydecarie/Dropbox (CEDIA)/simgem/simgen/simgen')
import data

sys.path.append('/Users/ydecarie/Dropbox (CEDIA)/simgem/simgen')
path_data = '/Users/ydecarie/Dropbox (CEDIA)/simgem/Benchmark/'
from simgen import model
yr_debut=2017
yr_fin=2020
base = model(start_yr=yr_debut,stop_yr=yr_fin)
base = model(start_yr=yr_debut,stop_yr=yr_fin)
base.startpop('/Users/ydecarie/Dropbox (CEDIA)/simgem/simgen/tests/startpopiso')
base.immig_assumptions(init='newimmpopiso')
base.birth_assumptions(scenario='reference')
base.dead_assumptions(scenario='low')
base.simulate(rep=1)
donnees=base.stats.counts
print('aaa')