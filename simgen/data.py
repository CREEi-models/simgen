import pandas as pd
import numpy as np
from multiprocessing import Pool as pool
from multiprocessing import cpu_count
from functools import partial
from os import path
import pickle
from inspect import currentframe, getframeinfo
from pandas.core.common import SettingWithCopyError
params_dir = path.join(path.dirname(__file__), 'params/')

def bdsps(file,year=2017,iprint=False, file_format='.dta'):

    """
    Nettoyage de la BDSPS.

    Fonction qui permet de mettre en forme la BDSPS.

    Parameters
    ----------
    year: int
        année de la base de départ (défaut=2017)
    iprint: boolean
        switch pour imprimer ou non des outputs intermédiaires de cette fonction (défaut=False)
    """
    if file_format=='.dta':
        df = pd.read_stata(file,convert_categoricals=False)
    if file_format==".csv":
        df = pd.read_csv(file)
    """
    df = df[df.hdprov==4]
    df = df[['hdseqhh','hdwgthh','hdwgthhs','idefseq','idefrh','hhnef','idage','idspoflg',
        'idimmi','idedlev','idestat','idmarst','efnkids','imqndc','hdnkids','idsex']]
    keep = []
    keys = df.groupby(['hdseqhh','idefseq']).count()['hdwgthh'].to_frame()
    keys.columns = ['ncount']
    keys['hhid'] = np.arange(len(keys))
    keys = keys.reset_index()
    df = df.merge(keys,left_on=['hdseqhh','idefseq'],right_on=['hdseqhh','idefseq'],how='left')
    keep.append('hhid')
    df['age'] = df.loc[:,'idage']
    df['age'] = np.where(df['age']==0,0,df['age'])
    keep.append('age')
    df['byr'] = year - df['age']
    df['byr'] = np.where(df['byr']>year,year,df['byr'])
    df['byr'].describe()
    keep.append('byr')
    df['male'] = df.idsex.replace({0:True,1:False})
    keep.append('male')
    df['immig'] = df.idimmi!=99
    df['newimm'] = df.idimmi<10
    df['yrsimm'] = df.idimmi.replace(99,np.nan)
    keep.append('immig')
    keep.append('newimm')
    keep.append('yrsimm')
    educ = {0:'none',1:'none',2:'none',3:'none',4:'none',5:'none',6:'des',
            7:'des',8:'dec',9:'dec',10:'uni',11:'uni',12:'uni'}
    df['educ4'] = df.idedlev.replace(educ)
    keep.append('educ4')
    df['inschool'] = df.idestat.replace({0:False,1:True,2:True,3:True})
    df.loc[df['age']==5,'inschool'] = True
    df.loc[df['age']>35,'inschool'] = False
    keep.append('inschool')
    df['married'] = df['idmarst'].replace({0:True,1:True,2:False,3:False,4:False,5:False})
    keep.append('married')
    df['spflag'] = df.loc[:,'idspoflg']
    keep.append('spflag')
    df['wgt'] = df.loc[:,'hdwgthh']
    totpop = df['wgt'].sum()
    keep.append('wgt')
    df['pn'] = df.loc[:,'idefrh'].astype('Int64')
    keep.append('pn')
    df['nas'] = np.arange(len(df))
    df['nas'] = df['nas'].astype('Int64')
    keep.append('nas')
    df['risk_iso']=False
    keep.append('risk_iso')
    # for each nas in df (dominant), drop adults in households, including chidlren
    # older than 18.
    pop = df.loc[df['pn']!=3,keep]
    kids18p = (pop.age>=18) & (pop.pn==2)
    #pop = pop[kids18p!=True]
    # calibrate weights by age and sex
    samp = pop.groupby(['age','male']).sum()['wgt'].unstack()
    samp.columns = ['female','male']
    samp = samp[['male','female']]
    cens = isq(year)
    totpop = cens.sum().sum()
    cens = cens[cens.index!=100]
    wgt = cens/samp
    wgt.columns = [True,False]
    wgt = wgt.stack()
    wgt.index.names = ['age','male']
    wgt = wgt.reset_index()
    wgt.columns = ['age','male','adj']
    pop = pop.merge(wgt,on=['age','male'])
    pop['wgt'] = pop['wgt'] * pop['adj']
    pop['wgt'] *= totpop/pop['wgt'].sum()
    pop = pop.drop(columns=['adj'])
    pop.to_csv('/Users/ydecarie/Documents/GitHub/simgen/simgen/start_pop/bdsps2017_slice.csv')
    """
    # dominants
    hh = df.copy()

    # spouses
    sps = hh.loc[hh.pn!=2,:].copy()
    keys = sps[['hhid','pn','nas']]
    keys.columns = ['hhid','pn_dom','nas_dom']
    sps.loc[:,'pn_dom'] = 1-sps.loc[:,'pn'].values
    sp = sps.merge(keys,left_on=['hhid','pn_dom'],right_on=['hhid','pn_dom'],how='left')
    sp = sp[sp.nas_dom.isna()==False]
    sp['nas'] = sp['nas_dom']
    sp = sp.drop(labels=['nas_dom','pn_dom'],axis=1)

    # kids
    kds = hh.loc[hh.pn==2,:]
    kds = kds[kds.age<18]
    keys = hh.loc[hh.pn!=2,['hhid','nas']]
    keys.columns = ['hhid','nas_dom']
    fams = keys.groupby(keys['hhid']).count()
    fams.columns = ['nparents']
    kds = kds.merge(fams['nparents'],left_on=['hhid'],right_index=True,how='left')

    # kids with one parent
    kds_1p = kds.loc[kds['nparents']==1,:]
    kids_1p = kds_1p.merge(keys,left_on=['hhid'],right_on=['hhid'],how='left')
    kids_1p['nas'] = kids_1p['nas_dom']
    kids_1p = kids_1p.drop(labels=['nas_dom'],axis=1)

    # kids with two parents
    kds_2p = kds.loc[kds['nparents']==2,:]
    sps = hh.loc[hh.pn!=2,:]
    keys = sps[['hhid','pn','nas']]
    keys.columns = ['hhid','pn_dom','nas_dom']
    keys_0 = keys.loc[keys.pn_dom==0,:]
    keys_1 = keys.loc[keys.pn_dom==1,:]
    kds_2p_0 = kds_2p.merge(keys_0,left_on='hhid',right_on='hhid',how='inner')
    kds_2p_1 = kds_2p.merge(keys_1,left_on='hhid',right_on='hhid',how='inner')
    kids_2p = kds_2p_0.append(kds_2p_1)
    kids_2p['nas'] = kids_2p['nas_dom']
    kids_2p = kids_2p.drop(labels=['pn_dom','nas_dom'],axis=1)

    # join back datasets
    kd = kids_1p.append(kids_2p)

    # index
    hh = hh.set_index('nas').sort_index()
    sp = sp.set_index('nas').sort_index()
    kd = kd.set_index('nas').sort_index()

    # one case of an individual with spflag=1 but no spouse: drop flag
    check = hh.merge(sp['byr'],left_index=True,right_index=True,how='left',suffixes=('','_sp'))
    tocorrect = check.loc[(check.spflag==1) & (check.byr_sp.isna()==True)].index
    hh.loc[tocorrect,'spflag'] = 0

    # modify the married variable to match the spouse variable (some weird cases of separated but
    # living in same household)

    hh.married = hh.spflag==1

    # add variable number of kids to dominant dataset
    nkids = kd.groupby('nas').count()['age']
    nkids.name = 'nkids'
    hh = hh.merge(nkids,left_index=True,right_index=True,how='left')
    hh.nkids = np.where(hh.nkids.isna(),0,hh.nkids)
    return hh,sp,kd

def isq(year):
    """
    Population par âge de l'ISQ.

    Fonction qui permet d'obtenir la population par âge de l'ISQ.

    Parameters
    ----------
    year: int
        année pour la population
    Returns
    -------
    dataframe
        dataframe *pandas* contenant la population par âge (hommes et femmes)
    """
    df = pd.read_excel(params_dir+'QC-age-sexe.xlsx',sheet_name='age',header=None,na_values='..')
    columns = ['year','niv','sex','total']
    for a in range(0,101):
        columns.append(a)
    columns.append('median')
    columns.append('mean')
    df.columns = columns
    df = df[(df['year']==year) & (df['sex']!=3)]
    df = df[[a for a in range(0,101)]].transpose()
    df.columns = ['male','female']
    df.index.name = 'age'
    return df


class parse:
    """
    Mise en forme des variables pour référence de SimGen.

    Classe qui permet de prendre un dataframe provenant d'une base de données particulière et retourner un dataframe propre interprétable par SimGen. On peut faire correspondre les noms de variables avec l'initialisation de la classe en utilisant les dictionnaires *map_hh*, *map_sp* et *map_kd* pour les trois registres.

    """
    def __init__(self):
        # Add iso_smaf if included in transitions
        self.vars_hh = ['wgt','byr','male','educ','insch','nkids','married','risk_iso']
        self.map_hh = dict(zip(self.vars_hh,self.vars_hh))
        self.vars_sp = ['byr','male','educ','insch']
        self.map_sp = dict(zip(self.vars_sp,self.vars_sp))
        self.vars_kd = ['byr','male','insch']
        self.map_kd = dict(zip(self.vars_kd,self.vars_kd))
        return
    def dominants(self,data):
        """
        Mise en forme des dominants.

        Fonction membre qui permet de prendre un dataframe dominant et d'appliquer les dictionnaires *map_hh* pour les noms de variables qui concordent avec SimGen.

        Parameters
        ----------
        data: dataframe
            dataframe de dominants
        Returns
        -------
        dataframe
            dataframe avec les noms de variables de SimGen
        """
        hh = pd.DataFrame(index=data.index,columns=self.vars_hh)
        for m in self.vars_hh:
            if self.map_hh[m] in data.columns:
                hh[m] = data[self.map_hh[m]]
        hh.index.name = 'nas'
        self.hh = hh
        hh.wgt = hh.wgt.astype(np.float64)
        hh.nkids = hh.nkids.astype('Int64')
        return hh
    def spouses(self,data):
        """
        Mise en forme des conjoints.

        Fonction membre qui permet de prendre un dataframe conjoint et d'appliquer les dictionnaires *map_sp* pour les noms de variables qui concordent avec SimGen.

        Parameters
        ----------
        data: dataframe
            dataframe de conjoints
        Returns
        -------
        dataframe
            dataframe avec les noms de variables de SimGen
        """
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
        """
        Mise en forme des enfants.

        Fonction membre qui permet de prendre un dataframe enfants et d'appliquer les dictionnaires *map_kd* pour les noms de variables qui concordent avec SimGen.

        Parameters
        ----------
        data: dataframe
            dataframe d'enfants
        Returns
        -------
        dataframe
            dataframe avec les noms de variables de SimGen
        """
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
    """
    Structure de population.

    Cette classe permet d'abriter sous un seul toit les dominants, conjoints et enfants et permet certaines opérations.

    """
    def __init__(self):
        return
    def input(self,hh,sp,kd):
        """
        Fonction pour entrer les registres.

        Fonction qui permet d'entrer les registres dominants, conjoints et enfants qui ont été préalablement passés dans *parse()*.

        Parameters
        ----------
        hh: dataframe
            dataframe des dominants
        sp: dataframe
            dataframe des conjoints
        kd: dataframe
            dataframe des enfants
        """
        self.hh = hh
        self.sp = sp
        self.kd = kd
        return
    def load(self,file):
        handler = open(file+'.pkl', 'rb')
        pop = pickle.load(handler)
        return pop
    def save(self,file):
        handler = open(file+'.pkl', 'wb')
        pickle.dump(self,handler, protocol=3)
        return
    def size(self,w=True):
        if w:
            return self.hh['wgt'].sum()
        else:
            return len(self.hh)
    def gennas(self,n):
        maxnas = self.hh.index.max()
        return np.arange(maxnas+1,maxnas+1+n)
    def enter(self,imm,year,ntarget):
        nimm = len(imm.hh)
        nwgt = imm.hh.wgt.sum()
        #if year<2043:
        #    ntarget= ntarget+(7.268e-5*(year-2017))
        #else:
        #    ntarget= ntarget+(7.268e-5*(25))
        imm.hh.wgt = imm.hh.wgt * (ntarget*self.hh.wgt.sum())/nwgt
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

class formating:
    """
    Organisation de la base de données.

    Cette classe permet de créer les fichiers nécessaires à la 
    simulation avec la base de départ BDSPS_ 2017.

    """

    def __init__(self):
        return
    def bdsps_format(self, data):
        hh,sp,kd = bdsps(data, file_format='.csv')
        imm = hh[hh.newimm]
        imm_nas = imm.index
        sp_imm = sp.loc[sp.index.isin(imm_nas),:]
        kd_imm = kd.loc[kd.index.isin(imm_nas),:]
        parsing = parse()
        parsing.map_hh['educ'] = 'educ4'
        parsing.map_sp['educ'] = 'educ4'
        parsing.map_hh['insch'] = 'inschool'
        parsing.map_sp['insch'] = 'inschool'
        parsing.map_kd['insch'] = 'inschool'
        hh = parsing.dominants(hh)
        sp = parsing.spouses(sp)
        kd = parsing.kids(kd)
        imm = parsing.dominants(imm)
        sp_imm = parsing.spouses(sp_imm)
        kd_imm = parsing.kids(kd_imm)
        pop = population()
        pop.input(hh,sp,kd)
        imm_pop = population()
        imm_pop.input(imm,sp_imm,kd_imm)
        pop.save('start_pop')
        imm_pop.save('imm_pop')