import warnings
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import sys
import os

sys.path.append('/Users/ydecarie/Documents/GitHub/simgen')
from simgen import model, formating , replicate

donnees_brutes = '/Users/ydecarie/Documents/GitHub/simgen/simgen/start_pop/bdsps2017_slice.csv'
annee_fin = 2040
fecondite = 'reference'
mortalite = 'low'
taux_immigration = 0.0066

preparation_data=formating()
preparation_data.bdsps_format(donnees_brutes)

base = model(stop_yr=(annee_fin-1),iomp=False)
base.startpop('start_pop')
base.immig_assumptions(init='imm_pop', num=taux_immigration)
base.birth_assumptions(scenario=fecondite)
base.dead_assumptions(scenario=mortalite)

exp = replicate(nreps=10,ncpus=1)

exp.set_model(base)
exp.simulate()