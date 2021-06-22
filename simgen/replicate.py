import numpy as np
from numba import njit
from multiprocessing import Pool as pool
from multiprocessing import cpu_count
from functools import partial
from simgen import update, population, statistics, model
import pandas as pd
from copy import deepcopy
from random import choices
from os import path
params_dir = path.join(path.dirname(__file__), 'params/')


class replicate:
	def __init__(self,nreps=1,ncpus=1):
		self.nreps = nreps
		self.ncpus = ncpus
		return 
	
	def set_model(self,model_base):
		self.model = model_base
		self.models = []
		for i in range(self.nreps):
			self.models.append(deepcopy(self.model))
		return 
	def run_model(self,m):
		m.simulate()
		return m.stats.counts
	def simulate(self):
		if self.ncpus>1:
			stats = []
			p = pool(self.ncpus)
			runs = [p.apply_async(self.run_model,args=(m,)) for m in self.models]
			for r in runs:
				stats.append(r.get())
		else :
			stats = [self.run_model(m) for m in self.models]
		self.stats = stats
		for i,r in enumerate(self.stats):
			r['rep'] = i
		self.stats = pd.concat(self.stats,axis=0)
		ids_old = list(self.stats.index.names)
		ids = ['rep']
		for i in ids_old:
			ids.append(i)
		self.stats = self.stats.reset_index()
		self.stats.set_index(ids,inplace=True)
		return 
	def save(self,file,imean=True,isd=True):
		self.stats.to_pickle(file+'.pkl',protocol=4)
		if imean:
			means = self.stats.groupby(level=list(self.stats.index.names)[1:]).mean()
			means.to_pickle(file+'_mean.pkl')
		if isd:
			sds = self.stats.groupby(level=list(self.stats.index.names)[1:]).std()
			sds.to_pickle(file+'_sd.pkl')
		return 
	def set_statistics(self,stratas=['age','male','insch','educ','married','nkids','risk_iso']):
		"""
		Fonction déterminant les variables de sortie.

		Parameters
		----------
		stratas : list
		Liste des variables de sortie
		"""
		return statistics(stratas)
	def freq(self,strata=None,bins=[0],sub=None):
		freqs = []
		for r in range(self.nreps):
			s = self.set_statistics()
			s.counts = self.stats.loc[self.stats.index.get_level_values(0)==r,:]
			if strata!=None:
				freq = s.freq(strata,bins,sub)
			else :	
				freq = s.freq(strata,bins,sub).to_frame()
				freq.columns= ['pop']
			freq.loc[:,'rep'] = r 
			freqs.append(freq)
		freqs = pd.concat(freqs,axis=0)
		freqs = freqs.reset_index()
		freqs.set_index(['index','rep'],inplace=True)
		return {'mean':freqs.groupby(level=0).mean(), 'sd':freqs.groupby(level=0).std()}

		


	