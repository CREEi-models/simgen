import pandas as pd 
import numpy as np 
from tools.actors import person, spouse, kid
from multiprocessing import Pool as pool 
from multiprocessing import cpu_count
from functools import partial 

def bdsps(file,year=2017,iprint=False):
    df = pd.read_stata(file,convert_categoricals=False)
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
    df['male'] = df.idsex.replace({1:True,0:False})
    keep.append('male')
    df['immig'] = df.idimmi!=99
    df['newimm'] = df.idimmi<10
    df['yrsimm'] = df.idimmi.replace(99,np.nan)
    keep.append('immig')
    keep.append('newimm')
    keep.append('yrsimm')
    educ = {0:'none',1:'none',2:'none',3:'none',4:'none',5:'none',6:'des',
            7:'des',8:'des',9:'dec',10:'dec',11:'uni',12:'uni'}
    df['educ4'] = df.idedlev.replace(educ)
    keep.append('educ4')
    df['inschool'] = df.idestat.replace({0:False,1:True,2:True,3:True})
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
    
    # dominants
    hh = pop.copy()
    
    # spouses
    sps = hh.loc[hh.pn!=2,:]
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
    df = pd.read_excel('../raw/isq/QC-age-sexe.xlsx',sheet_name='age',header=None,na_values='..')
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
    
