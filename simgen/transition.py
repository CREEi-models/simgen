import numpy as np
from numba import njit,jit,int64,float64
from simgen import population
import pandas as pd
from multiprocessing import Pool
from multiprocessing import cpu_count
from random import choices
from functools import partial
from os import path
params_dir = path.join(path.dirname(__file__), 'params/')

class update:
    """
    Classe pour les transitions.

    Classe permettant d'effectuer différentes transitions d'une année à l'autre.

    """
    def __init__(self,iomp=False):
        self.iomp = iomp 
        self.map_edu = {'none':0,'des':1,'dec':2,'uni':3}
        self.imap_edu = {0:'none',1:'des',2:'dec',3:'uni'}
        self.params_birth()
        self.params_dead('medium')
        self.params_union()
        self.params_divorce()
        self.params_schldone()
        self.params_educ()
        self.params_emig()
        self.params_risk_iso(params_set=1)
        return
    def params_birth(self):
        """
        Chargement des paramètres pour transitions de naissances.

        Le chargement est fait automatiquement avec la création d'une instance de la classe.

        """
        df = pd.read_csv(params_dir+'trans_births.csv',sep=';')
        df.columns = ['var',1,2,3]
        df = df.set_index('var')
        self.par_birth = df.transpose()
        return
    def params_union(self):
        """
        Chargement des paramètres pour transitions d'unions.

        Le chargement est fait automatiquement avec la création d'une instance de la classe.

        """
        df = pd.read_csv(params_dir+'trans_unions.csv',sep=';')
        df = df.set_index('var')
        self.par_union = df['m']
        return
    def params_divorce(self):
        """
        Chargement des paramètres pour transitions de séparations.

        Le chargement est fait automatiquement avec la création d'une instance de la classe.

        """
        df = pd.read_csv(params_dir+'trans_divorces.csv',sep=';')
        df = df.set_index('var')
        self.par_divorce = df['d']
        return
    def params_dead(self,scn):
        """
        Chargement des paramètres pour transitions de mortalité.

        Le chargement est fait automatiquement avec la création d'une instance de la classe.

        """
        df = pd.read_csv(params_dir+'trans_mortality_'+scn+'.csv',sep=';')
        columns = ['year','male','prov']
        for a in range(0,111):
            columns.append(a)
        df.columns = columns
        df = df.drop(columns=['prov'])
        df['male'] = df['male'].replace({1:True,0:False})
        df = df.set_index(['year','male'])
        df.columns = pd.Index(df.columns)
        df.columns.name = 'age'
        df = df.stack()
        df.name = 'rate'
        df = df.to_frame()
        self.mx = df
        df2 = pd.read_csv(params_dir+'trans_death_chsld.csv',sep=',')
        df2.columns = ['var','value']
        df2['var'] = df2['var'].apply(str)
        df2 = df2.set_index('var')
        df2.name='chsld'
        self.par_chsld = df2
        df3 = pd.read_csv(params_dir+'trans_death_home.csv',sep=',')
        df3.columns = ['var','value']
        df3['var'] = df3['var'].apply(str)
        df3 = df3.set_index('var')
        df3.name='home'
        self.par_home = df3
        return
    def params_schldone(self):
        """
        Chargement des paramètres pour transitions de fin de scolarité.

        Le chargement est fait automatiquement avec la création d'une instance de la classe.

        """
        df = pd.read_csv(params_dir+'trans_schldone.csv',sep=';')
        df.columns = ['var','value']
        df = df.set_index('var')
        self.par_schldone = df.loc[:,'value']
        return
    def params_educ(self):
        """
        Chargement des paramètres pour transitions de fin d'études.

        Le chargement est fait automatiquement avec la création d'une instance de la classe.

        """
        df = pd.read_csv(params_dir+'trans_degree.csv',sep=';')
        df.columns = ['var','none','dec','uni']
        df = df.set_index('var')
        df['des'] = 0.0
        self.par_educ = df
        return
    def params_emig(self):
        """
        Chargement des paramètres pour transitions d'émigration.

        Le chargement est fait automatiquement avec la création d'une instance de la classe.

        """
        df = pd.read_csv(params_dir+'tx_em_age.csv',sep=';')
        df.columns = ['var','value']
        df = df.set_index('var')
        df['value'] = df['value']*1e-3
        self.par_emig = df.loc[:,'value']
        return


    def params_risk_iso(self,params_set=1):
        """
        Chargement des paramètres pour le risque d'être dans la population iso'.

        Le chargement est fait automatiquement avec la création d'une instance de la classe.

        """
        df = pd.read_csv(params_dir+'risk_iso.csv',sep=';')
        df.columns = ['var','risk_iso1']
        df = df.set_index('var')
        self.par_risk_iso = df.loc[:,'risk_iso'+str(params_set)]
        return

    def birth(self,pop,year,ntarget):
        """
        Fonction de transitions pour les naissances.

        Parameters
        ----------
        pop: population
            population (instance de la classe population)
        year: int
            année de la transition
        ntarget: int
            nombre de naissances visé (si alignement)

        Returns
        -------
        population
            instance de la classe population
        """
        # make sure ages have been updated
        pop.ages(year)
        # define who is eligible
        elig = pop.hh[(pop.hh['married']) & (pop.hh['age']>=18)].index.to_list()
        # find number of kids and age of youngest kid
        pop.nkids()
        pop.kagemin()
        # get set with joint characteristics
        work = pop.merge_spouses()
        work = work.loc[work.index.isin(elig),
                        ['age','age_sp','educ','educ_sp','male','insch','nkids','agemin']]
        # create covariates
        covars = ['dage2529','dage3034','dage3539','dage40p','lkidage','insch','des','dec','uni','constant']
        work['rank'] = work['nkids']+1
        work['rank'] = np.where(work['rank']>3,3,work['rank'])
        work['age'] = np.where(work.male,work.age_sp,work.age)
        work['educ'] = np.where(work.male,work.educ_sp,work.educ)
        work['des'] = work['educ']=='des'
        work['dec'] = work['educ']=='dec'
        work['uni'] = work['educ']=='uni'
        work['dage2529'] = (work['age']>=25) & (work['age']<=29)
        work['dage3034'] = (work['age']>=30) & (work['age']<=34)
        work['dage3539'] = (work['age']>=35) & (work['age']<=39)
        work['dage40p'] = (work['age']>=40)
        work['lkidage'] = work['agemin']
        work['constant'] = 1
        # compute probability
        work['pr'] = 0.0
        for v in covars:
            work['pr'] += work[v].multiply(self.par_birth.loc[work['rank'],v].values)
        work['pr'] = np.exp(work['pr'])/(1+np.exp(work['pr']))
        work['pr'] = np.where(work['age']>=45,0,work['pr'])
        # draw new births
        work['birth'] = np.random.uniform(size=len(work))<work['pr']
        nbirths = work['birth'].sum()
        # create new kids
        nas_newparents = work[work['birth']].index.to_list()
        newkids = pd.DataFrame(index=nas_newparents,columns=pop.kd.columns)
        newkids.index.name = 'nas'
        newkids['byr'] = year
        newkids['male'] = np.random.uniform(size=nbirths)<0.512
        newkids['insch'] = False
        newkids['age'] = 0
        # append kids to kids dataset and update globals for dominants
        pop.kd = pop.kd.append(newkids)
        pop.nkids()
        pop.kagemin()
        # create dominants
        maxnas = pop.hh.index.max()
        newnas = [a for a in range(maxnas+1,maxnas+1+nbirths)]
        newdoms = pd.DataFrame(index=newnas,columns=pop.hh.columns)
        newdoms.index.name = 'nas'
        newdoms['wgt'] = ntarget/nbirths
        newdoms['byr'] = year
        newdoms['male'] = np.random.uniform(size=nbirths)<0.5
        newdoms['educ'] = 'none'
        newdoms['insch'] = False
        newdoms['nkids'] = 0
        newdoms['married'] = False
        newdoms['age'] = 0
        newdoms['agemin'] = 0
        newdoms['risk_iso'] = False
        #newdoms['iso_smaf'] = -1
        pop.hh = pop.hh.append(newdoms)
        return pop

    def match(self,grooms,pop):
        nas_grooms = grooms.index.to_list()
        newsp = pd.DataFrame(index=nas_grooms,columns=pop.sp.columns)
        donors = pop.hh[pop.hh.married==True].sort_values(by=['educ','male'])
        for i in grooms.index:
            groom = grooms.loc[i,:]
            pool = (donors.educ==groom['educ']) & (donors.male == groom['male']) & (np.absolute(donors.byr-groom['byr'])<=5) 
            nas_pool = donors.loc[pool].index.to_list()
            if len(nas_pool)>0:
                nas_pick = choices(nas_pool,k=1)
                bride = pop.sp.loc[nas_pick[0],:]
            else :
                pool = (donors.educ==groom['educ']) & (donors.male == groom['male']) & (np.absolute(donors.byr-groom['byr'])<=20) 
                nas_pool = donors.loc[pool].index.to_list()
                nas_pick = choices(nas_pool,k=1)
                bride = pop.sp.loc[nas_pick[0],:]
            newsp.loc[i,:] = bride.to_list()
        return newsp

    def marriage(self,pop,year):
        """
        Fonction de transitions pour les formations d'unions.

        Parameters
        ----------
        pop: population
            population (instance de la classe population)
        year: int
            année de la transition

        Returns
        -------
        population
            instance de la classe population
        """
        pop.ages(year)
        cond = (pop.hh.married==False) & (pop.hh.age<=65) & (pop.hh.age>=18)
        work = pop.hh.loc[cond,['male','age','educ','insch','byr']]
        work['age1619'] = (work['age']>=16) & (work['age']<=19)
        work['age2024'] = (work['age']>=20) & (work['age']<=24)
        work['age2529'] = (work['age']>=25) & (work['age']<=29)
        work['age3539'] = (work['age']>=35) & (work['age']<=39)
        work['age4044'] = (work['age']>=40) & (work['age']<=44)
        work['age4549'] = (work['age']>=45) & (work['age']<=49)
        work['age5054'] = (work['age']>=50) & (work['age']<=54)
        work['age5559'] = (work['age']>=55) & (work['age']<=59)
        work['des'] = work['educ']=='des'
        work['dec'] = work['educ']=='dec'
        work['uni'] = work['educ']=='uni'
        work['constant'] = 1
        covars = ['male','age1619','age2024','age2529',
            'age3539','age4044','age4549','age5054','age5559','insch',
            'des','dec','uni','constant']
        work['pr'] = 0
        for v in covars:
            work['pr'] += work[v]*self.par_union[v]
        work['pr'] = np.exp(work['pr'])/(1+np.exp(work['pr']))
        work['wedding'] = np.random.uniform(size=len(work))<work['pr']
        grooms = work[work['wedding']].copy()
        nas_grooms = grooms.index.to_list()
        # find brides for the grooms by picking among pool of spouses
        f = partial(self.match,pop=pop)
        if self.iomp:
            ncores = cpu_count()
            grooms_split = np.array_split(grooms, ncores)
            p = Pool(ncores)
            newsp = pd.concat(p.map(f,grooms_split))
            p.close()
            p.join()
        else :
            donors = pop.hh.loc[pop.hh.married==True,['male','educ','byr']].copy()
            donors = donors.reset_index()
            donors.nas = donors.nas.astype('int64')
            grooms = grooms.loc[:,['male','educ','byr']].copy()
            grooms = grooms.reset_index()
            grooms.nas = grooms.nas.astype('int64')
            grooms['nas_bride'] = 0
            for m in [False,True]:
	            for e in ['none','des','dec','uni']:
		            g = grooms.loc[(grooms.male==m) & (grooms.educ==e),['byr','nas']]
		            d = donors.loc[(donors.male==m) & (donors.educ==e),['byr','nas']]
		            nas_sp = match_jit(g.nas.to_numpy(),d.nas.to_numpy(),g.byr.to_numpy(),d.byr.to_numpy())
		            grooms.loc[(grooms.male==m) & (grooms.educ==e),'nas_bride'] = nas_sp 
            nas_brides = grooms.nas_bride.to_list()
            newsp = pd.DataFrame(index=grooms.nas.to_list(),columns=pop.sp.columns)
            newsp = pop.sp.loc[pop.sp.index.isin(nas_brides),:] 
        # grooms become married
        pop.hh.loc[nas_grooms,'married'] = True
        # brides added to pool of spouses
        pop.sp = pop.sp.append(newsp)
        return pop

    def divorce(self,pop,year):
        """
        Fonction de transitions pour les dissolutions d'unions.

        Parameters
        ----------
        pop: population
            population (instance de la classe population)
        year: int
            année de la transition

        Returns
        -------
        population
            instance de la classe population
        """
        pop.ages(year)
        pop.nkids()
        cond = (pop.hh.married==True) & (pop.hh.age<=65) & (pop.hh.age>=18)
        work = pop.hh.loc[cond,['male','age','educ','byr','insch','nkids']]
        work['dmale'] = np.where(work['male'],1,0)
        work['mage']  = work['dmale']*work['age']
        work['mage2'] = work['dmale']*(work['age'].astype('float64')**2)
        work['mage3'] = work['dmale']*(work['age'].astype('float64')**3)
        work['wage']  = (1-work['dmale'])*work['age']
        work['wage2'] = (1-work['dmale'])*(work['age'].astype('float64')**2)
        work['wage3'] = (1-work['dmale'])*(work['age'].astype('float64')**3)
        work['des'] = work['educ']=='des'
        work['dec'] = work['educ']=='dec'
        work['uni'] = work['educ']=='uni'
        work['kid'] = work['nkids']>0
        work['constant'] = 1
        covars = ['male','mage','mage2','mage3','wage','wage2','wage3','des','dec','uni','insch','kid','constant']
        work['pr'] = 0
        for v in covars:
            work['pr'] += work[v]*self.par_divorce[v]
        work['pr'] = np.exp(work['pr'])/(1+np.exp(work['pr']))
        work['divorce'] = np.random.uniform(size=len(work))<work['pr']
        nas_divorced = work[work['divorce']].index.to_list()
        # dominant turns married off
        pop.hh.loc[nas_divorced,'married'] = False
        # drop spouses
        pop.sp = pop.sp.loc[~pop.sp.index.isin(nas_divorced)]
        return pop

    def risk_iso(self,pop,year):
        pop.ages(year)
        cond = pop.hh.age>=65
        pop.hh.loc[cond,'risk_iso']=False
        work = pop.hh.loc[cond,['male','age','risk_iso']]
        work['risk_iso']=False
        work['male_6569'] = (work['male']==True) & (work['age']>=65) & (work['age']<=69)
        work['male_7074']  = (work['male']==True) & (work['age']>=70) & (work['age']<=74)
        work['male_7579']  = (work['male']==True) & (work['age']>=75) & (work['age']<=79)
        work['male_80p']  = (work['male']==True) & (work['age']>=80)
        work['female_6569']  = (work['male']==False) & (work['age']>=65) & (work['age']<=69)
        work['female_7074']  = (work['male']==False) & (work['age']>=70) & (work['age']<=74)
        work['female_7579']  = (work['male']==False) & (work['age']>=75) & (work['age']<=79)
        work['female_80p']  = (work['male']==False) & (work['age']>=80)
        covars = ['male_6569','male_7074','male_7579','male_80p','female_6569','female_7074','female_7579','female_80p']
        work['pr'] = 0.0
        for v in covars:
            work['pr'] += work[v]*self.par_risk_iso[v]
        work['rand']= np.random.uniform(size=len(work))
        cond = work['rand']<work['pr']
        work.loc[cond,'risk_iso']=True
        nas_risk_iso = work[work['risk_iso']==True].index.to_list()
        pop.hh.loc[nas_risk_iso,'risk_iso'] = True
        return pop

    def dead(self,pop,year):
        """
        Fonction de transitions pour les décès.

        Parameters
        ----------
        pop: population
            population (instance de la classe population)
        year: int
            année de la transition

        Returns
        -------
        population
            instance de la classe population
        """
        # make sure year up to date
        pop.ages(year)
        work = pop.hh.loc[:,['male','age']]
        work['year'] = year
        #work = work.merge(self.par_ajust_chsld,on=['age'],how='left')
        work['factor_home']=1
        work['factor_chsld']=1
        work = work.merge(self.mx,left_on=['year','male','age'],right_index=True,how='left')
        #na_val = {'factor_home':1,'factor_chsld':1}
        #work = work.fillna(value=na_val)
        work['factor']=1
        work['dead'] = np.random.uniform(size=len(work))<(work['rate']*work['factor'])
        #work['test_rate'] = (work['rate']*work['factor'])
        nas_dead = work[work['dead']].index.to_list()
        pop.hh = pop.hh[~pop.hh.index.isin(nas_dead)]
        pop.sp = pop.sp[~pop.sp.index.isin(nas_dead)]
        pop.kd = pop.kd[~pop.kd.index.isin(nas_dead)]
        return pop
    def sp_dead(self,pop,year):
        pop.ages(year)
        work = pop.sp.loc[:,['male','age']]
        work['year'] = year
        work = work.merge(self.mx,left_on=['year','male','age'],right_index=True,how='left')
        work['dead'] = np.random.uniform(size=len(work))<work['rate']
        nas_dead = work[work['dead']].index.to_list()
        pop.sp = pop.sp[~pop.sp.index.isin(nas_dead)]
        pop.hh.loc[nas_dead,'married'] = False
        return pop
    def kids_dead(self,pop,year):
        pop.ages(year)
        work = pop.kd.loc[:,['male','age']]
        work['year'] = year
        work = work.merge(self.mx,left_on=['year','male','age'],right_index=True,how='left')
        work['dead'] = np.random.uniform(size=len(work))<work['rate']
        nas_dead = work[work['dead']].index.to_list()
        pop.kd = pop.kd[~pop.kd.index.isin(nas_dead)]
        pop.nkids()
        pop.kagemin()
        return pop
    def moveout(self,pop,year):
        pop.ages(year)
        pop.kd = pop.kd[pop.kd.age<18]
        pop.nkids()
        pop.kagemin()
        return pop
    def emig(self,pop,year):
        """
        Fonction de transitions pour gérer l'émigration.

        Parameters
        ----------
        pop: population
            population (instance de la classe population)
        year: int
            année de la transition

        Returns
        -------
        population
            instance de la classe population
        """
        pop.ages(year)
        work = pop.hh.loc[:,['age','male']]
        ages = [(0,4),(5,9),(10,14),(15,19),(20,24),(25,29),(30,34),
            (35,39),(40,44),(45,49),(50,54),(55,59),(60,64),(65,69),
            (70,74),(75,79),(80,84),(85,89),(90,110)]
        names = self.par_emig.index.to_list()
        work['pr'] = 0.0
        for i,a in enumerate(ages):
            work['pr'] = np.where((work['age']>=a[0]) & (work['age']<=a[1]),
                self.par_emig[names[i]],work['pr'])
        u = np.random.uniform(size=len(work))
        work['emig'] = u<work['pr']
        nas_emig = work[work['emig']].index.to_list()
        popemmig=  pop.hh.loc[pop.hh.index.isin(nas_emig)]
        tot = popemmig.sum()
        pop.hh = pop.hh.loc[~pop.hh.index.isin(nas_emig)]
        pop.sp = pop.sp.loc[~pop.sp.index.isin(nas_emig)]
        pop.kd = pop.kd.loc[~pop.kd.index.isin(nas_emig)]
        return pop
    def educ(self,pop,year):
        """
        Fonction de transitions pour changements de niveau d'éducation.

        Parameters
        ----------
        pop: population
            population (instance de la classe population)
        year: int
            année de la transition

        Returns
        -------
        population
            instance de la classe population
        """
        pop.ages(year)
        pop.nkids()
        # deal first with those entering school
        pop.hh.loc[pop.hh.age==5,'insch'] = True
        pop.kd.loc[pop.kd.age==5,'insch'] = True
        # force quitting school after 35
        pop.hh.loc[pop.hh.age>35,'insch'] = False
        # now those who quit (probabilistic)
        selection = (pop.hh.insch) & (pop.hh.age>=17) & (pop.hh.age<=35)
        work = pop.hh.loc[selection,['age','male','nkids']]
        work['mother'] = (work['nkids']>0)*(work['male']!=True)
        work['father'] = (work['nkids']>0)*(work['male'])
        #work['byear'] = year-work['age']
        beta = self.par_schldone
        work['pr'] = beta['constant']
        for a in range(18,36):
            work['pr'] += np.where(work['age']==a,beta['age'+str(a)],0.0)
        work['pr'] += beta['male']*work['male']
        work['pr'] += beta['mother']*work['mother']
        work['pr'] += beta['father']*work['father']
        #work['pr'] += beta['byear']*work['byear']
        work['pr'] = np.exp(work['pr'])/(1+np.exp(work['pr']))
        work['quit'] = np.random.uniform(size=len(work))<work['pr']
        work['quit'] = np.where(work['age']==35,True,work['quit'])
        quit = work[work['quit']].copy()
        if len(quit)>0:
            nas_quit = quit.index.to_list()
            states = ['none','des','dec','uni']
            beta = self.par_educ
            for s in states:
                quit[s] = beta.loc['constant',s]
                for a in range(18,36):
                    quit[s] += np.where(quit['age']==a,beta.loc['age'+str(a),s],0.0)
                quit[s] += beta.loc['male',s]*quit['male']
                quit[s] += beta.loc['mother',s]*quit['mother']
                quit[s] += beta.loc['father',s]*quit['father']
                quit[s] = np.exp(quit[s])
            quit['tot'] = quit[states].sum(axis=1)
            for s in states:
                quit[s] = quit[s]/quit['tot']
            f = partial(self.mlogit,states=states)
            quit['educ'] = quit.apply(f,axis=1)
            # assign back to households
            pop.hh.loc[nas_quit,'insch'] = False
            pop.hh.loc[nas_quit,'educ'] = quit.loc[:,'educ']
        return pop
    def mlogit(self,row,states):
        pr = row[states]
        s = np.random.choice(a=states,p=pr)
        return s

@njit
def pbirth(age,educ,agemin,beta):
    base = 0.0
    if age>=25 and age<=29:
        base += beta[0]
    if age>=30 and age<=34:
        base += beta[1]
    if age>=35:
        base += beta[2]
    base += agemin*beta[3]
    if educ==1:
        base += beta[4]
    if educ==2:
        base += beta[5]
    if educ==3:
        base += beta[6]
    base += beta[7]
    pr = np.exp(base)/(1.0+np.exp(base))
    if age>=45:
        pr= 0
    return pr



@njit
def pmarr(age,male,educ):
    return 0.0

@njit
def find_spouse(age,male,educ):
    sp_age = age-5
    sp_educ = educ
    return sp_age, sp_educ

@njit
def pdiv(age,sp_age,male,educ,sp_educ,nkids):
    return 0.0

@njit
def pdead(age,male):
    return 0.0

@njit
def pemig(age,male):
    return 0.0

@njit
def quit(age,male):
    return 0.0

@njit
def enroll(age,male):
    return 0.0

@njit
def pdes(age,male):
    return 0.0
@njit
def pdec(age,male):
    return 0.0
@njit
def puni(age,male):
    return 0.0

@jit(fastmath=True)
def match_jit(nas_grooms,nas_donors,byr_grooms,byr_donors):
	n = nas_grooms.shape[0]
	bride_nas = np.zeros(n)
	for i in range(n):
		d = np.abs(byr_grooms[i] - byr_donors)
		nas_pool = np.argsort(d)
		pick = np.random.choice(nas_pool[:5],size=1)
		bride_nas[i] = nas_donors[pick]
	return bride_nas