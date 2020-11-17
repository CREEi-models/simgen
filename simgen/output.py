import numpy as np
import pandas as pd
from itertools import product
class statistics:
    """
    Classe pour créer les statistiques provenant d'une simulation.

    Cette classe permet de capturer la distribution de la population par strate durant une simulation. Elle permet ensuite de faire plusieurs tableaux dynamiques à partir de ces distributions.

    Parameters
    ----------

    stratas: list of str
        liste des noms de variables du fichiers de dominants afin de stratifier la population et récolter les fréquences (pondérées)
    """
    def __init__(self,stratas):
        self.stratas = stratas
        self.counts = None
        self.mean_counts = pd.DataFrame({' ' : []})
        return
    def start(self,pop,year):
        """
        Initialisation de la distribution sur l'année de départ.

        Le membre de la classe qui contient les fréquences (*counts*) est populé pour l'année de départ.

        Parameters
        ----------
        pop: population
            population de départ (instance de la classe population)
        year: int
            année de départ de la simulation
        """
        list_value_column = [[i for i in range(1,111)]] #start with ages
        for col in ['male','insch','educ','married','nkids','iso_smaf']:
            list_value_column.append(pop.hh[col].sort_values().unique())
        empty = pd.DataFrame(list(product(*list_value_column)),
                             columns=['age','male','insch','educ','married','nkids','iso_smaf']).set_index(['age','male','insch','educ','married','nkids','iso_smaf'])
        empty[year]=0.0
        counts = pop.hh.groupby(self.stratas).sum()[['wgt']].fillna(0.0)
        counts = counts.rename(columns={'wgt':year})
        self.counts= empty.add(counts,fill_value=0.0)
        return
    def add(self,pop,year):
        """
        Fonction pour ajouter une année à la distribution.

        À chaque année d'une simulation, cette fonction est invoquée afin de récolter la distribution par strate dans l'année en cours. Cette population est ajoutée à *counts*.

        Parameters
        ----------
        pop: population
            population de départ (instance de la classe population)
        year: int
            année de départ de la simulation
        """
        counts = pop.hh.groupby(self.stratas).sum()['wgt']
        counts.name = year
        self.counts = self.counts.merge(counts,left_index=True,right_index=True,how='outer')
        self.counts = self.counts.fillna(0.0)
        return
    def add_to_mean(self,rep):
        """
        Fonction pour ajouter une réplication à la moyenne des distributions.

        À chaque réplication, les valeurs du aataFrame self.counts/nbr_réplication sont ajoutées à la moyenne des valeurs.

        Parameters
        ----------
        rep: nombre de réplications de la simulation
        """

        if self.mean_counts.empty:
            self.mean_counts = self.counts.copy()
            self.mean_counts[:] = 0
        self.mean_counts = self.mean_counts.add(self.counts/rep,fill_value=0)
        return

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
    def save(self,file):
        """
        Fonction pour sauvegarder les fichiers de fréquences.

        Parameters
        ----------
        file: str
            nom du fichier de sauvegarde, incluant l'extension pkl (format pickle)
        """
        self.counts.to_pickle(file,protocol=4)
        return
