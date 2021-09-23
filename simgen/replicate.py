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
	"""
    Modèle de simulation SimGen.

    Cette classe permet la parallélisation du calcul des différentes réplications.

    Parameters
    ----------
    nreps : int
        nombre de réplications (défaut=1)
    ncpus : int
        nombre de coeurs utilisés pour le calcul (défaut=1)
    """
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
		"""
        Fonction déclenchant le lancement de la simulation.

        Parameters
        ----------
    	"""
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
		"""
		Fonction pour sauvegarder les fichiers de fréquences.

		Sauvegarde de 3 fichiers : 1) *.pkl* avec les fréquences de l'ensemble des réplications 2) *_mean.pkl* avec les fréquences moyennes des réplications 3) *_sd.pkl* avec l'écart-type des fréquences des réplications

		Parameters
		----------
		file: str
			Nom du fichier de sauvegarde, incluant l'extension pkl (format pickle)
		"""
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
		"""
        Fonction de fréquences.

        Fonction qui permet, à l'aide de *counts*, de calculer les fréquences pondérées pour une strate donnée. Deux options sont disponibles: l'une, *bins*, permet de modifier les catégories de la strate (par exemple le groupe d'âge), tandis que *sub* permet de définir un critère de sélection particulier pour le calcul des fréquences (en str).

        Parameters
        ----------
        strata: str
            nom de la variable par laquelle on veut découper les données; ne pas spécifier cette option revient à demander les fréquences totales
        bins: list of int
            liste de valeurs pour découper les données selon la variable strata; fonctionne seulement avec des variables de types int (pas de str)
        sub: str
            condition à respecter pour un sous-échantillon, p.ex. \"age>=18\"
        Returns
        -------
        dataframe
            dataframe avec les fréquences par année (ligne) et valeur de la strate (colonne)
        """
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
	def prop(self,strata=None,bins=[0],sub=None):
		"""
        Fonction de proportions.

        Fonction qui permet, à l'aide de *counts*, de calculer les proportions pondérées pour une strate donnée. Deux options sont disponibles: l'une, *bins*, permet de modifier les catégories de la strate (par exemple le groupe d'âge), tandis que *sub* permet de définir un critère de sélection particulier pour le calcul des proportions (en str).

        Parameters
        ----------
        strata: str
            nom de la variable par laquelle on veut découper les données
        bins: list of int
            liste de valeurs pour découper les données selon la variable strata; fonctionne seulement avec des variables de types int (pas de str)
        sub: str
            condition à respecter pour un sous-échantillon, p.ex. \"age>=18\"
        Returns
        -------
        dataframe
            dataframe avec les proportions par année (ligne) et valeur de la strate (colonne)
        """
		freqs = []
		for r in range(self.nreps):
			s = self.set_statistics()
			s.counts = self.stats.loc[self.stats.index.get_level_values(0)==r,:]
			if strata!=None:
				freq = s.prop(strata,bins,sub)
			else :	
				freq = s.prop(strata,bins,sub).to_frame()
				freq.columns= ['pop']
			freq.loc[:,'rep'] = r 
			freqs.append(freq)
		freqs = pd.concat(freqs,axis=0)
		freqs = freqs.reset_index()
		freqs.set_index(['index','rep'],inplace=True)
		return {'mean':freqs.groupby(level=0).mean(), 'sd':freqs.groupby(level=0).std()}
		


	