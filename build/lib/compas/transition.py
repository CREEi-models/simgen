import numpy as np 
from numba import njit,int64,float64
from compas import population
import pandas as pd
from multiprocessing import Pool 
from multiprocessing import cpu_count
from random import choices
from functools import partial
from os import path
params_dir = path.join(path.dirname(__file__), 'params/')

class update: 
    def __init__(self):
        self.map_edu = {'none':0,'des':1,'dec':2,'uni':3}
        self.imap_edu = {0:'none',1:'des',2:'dec',3:'uni'}
        self.params_birth()
        self.params_dead('medium')
        self.params_union()
        self.params_divorce()
        self.params_schldone()
        self.params_educ()
        return
    def params_birth(self):
        df = pd.read_csv(params_dir+'trans_births.csv',sep=';')
        df.columns = ['var',1,2,3]
        df = df.set_index('var')
        self.par_birth = df.transpose()
        return
    def params_union(self):
        df = pd.read_csv(params_dir+'trans_unions.csv',sep=';')
        df = df.set_index('var')
        df = df.transpose()
        df = df.loc['m1',:]
        self.par_union = df
        return
    def params_divorce(self):
        df = pd.read_csv(params_dir+'trans_divorces.csv',sep=';')
        df = df.set_index('var')
        df = df.transpose()
        df = df.loc['d1',:]
        self.par_divorce = df
        return
    def params_dead(self,scn):
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
        return
    def params_schldone(self):
        df = pd.read_csv(params_dir+'trans_schldone.csv',sep=';')
        df.columns = ['var','value']
        df = df.set_index('var')
        self.par_schldone = df.loc[:,'value']
        return
    def params_educ(self):
        df = pd.read_csv(params_dir+'trans_degree.csv',sep=';')
        df.columns = ['var','none','dec','uni']
        df = df.set_index('var')
        df['des'] = 0.0
        self.par_educ = df
        return
    def birth(self,pop,year,ntarget):
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
        covars = ['dage2529','dage3034','dage35p','lkidage','insch','des','dec','uni','constant']
        work['rank'] = work['nkids']+1
        work['rank'] = np.where(work['rank']>3,3,work['rank'])
        work['age'] = np.where(work.male,work.age_sp,work.age)
        work['educ'] = np.where(work.male,work.educ_sp,work.educ)
        work['des'] = work['educ']=='des'
        work['dec'] = work['educ']=='dec'
        work['uni'] = work['educ']=='uni'
        work['dage2529'] = (work['age']>=25) & (work['age']<=29)
        work['dage3034'] = (work['age']>=30) & (work['age']<=34)
        work['dage35p'] = (work['age']>=35) 
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
        newkids['male'] = np.random.uniform(size=nbirths)<0.5
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
        pop.hh = pop.hh.append(newdoms)
        return pop
    def match(self,grooms,pop):
        nas_grooms = grooms.index.to_list()
        newsp = pd.DataFrame(index=nas_grooms,columns=pop.sp.columns)
        for i in grooms.index:
            groom = grooms.loc[i,:]
            pool = (pop.hh.married==True) & (pop.hh.educ==groom['educ']) & (np.absolute(pop.hh.byr-groom['byr'])<=5) & (pop.hh.male == groom['male'])
            nas_pool = pop.hh.loc[pool].index.to_list()
            if len(nas_pool)>0:
                nas_pick = choices(nas_pool,k=1)
                bride = pop.sp.loc[nas_pick[0],:]
            else :
                pool = (pop.hh.married==True) & (pop.hh.educ==groom['educ']) & (np.absolute(pop.hh.byr-groom['byr'])<=20) & (pop.hh.male == groom['male'])
                nas_pool = pop.hh.loc[pool].index.to_list()
                nas_pick = choices(nas_pool,k=1)
                bride = pop.sp.loc[nas_pick[0],:]
            newsp.loc[i,:] = bride.to_list()
        return newsp        
    def marriage(self,pop,year):
        pop.ages(year)
        cond = (pop.hh.married==False) & (pop.hh.age<=65) & (pop.hh.age>=18)
        work = pop.hh.loc[cond,['male','age','educ','insch','byr']]
        work['mage'] = work['male']*work['age']
        work['mage2'] = work['male']*work['age'].astype('float64')**2
        work['wage'] = (work['male']==False)*work['age']
        work['wage2'] = (work['male']==False)*work['age'].astype('float64')**2
        work['des'] = work['educ']=='des'
        work['dec'] = work['educ']=='dec'
        work['uni'] = work['educ']=='uni'
        work['constant'] = 1
        covars = ['male','mage','mage2','wage','wage2','insch','des','dec','uni','constant']
        work['pr'] = 0
        for v in covars: 
            work['pr'] += work[v]*self.par_union[v]
        work['pr'] = np.exp(work['pr'])/(1+np.exp(work['pr']))
        work['wedding'] = np.random.uniform(size=len(work))<work['pr']
        grooms = work[work['wedding']]
        nas_grooms = grooms.index.to_list()
        # find brides for the grooms by picking among pool of spouses
        f = partial(self.match,pop=pop)
        ncores = cpu_count()
        grooms_split = np.array_split(grooms, ncores)
        p = Pool(ncores)
        newsp = pd.concat(p.map(f,grooms_split))
        p.close()
        p.join()
        # grooms become married
        pop.hh.loc[nas_grooms,'married'] = True
        # brides added to pool of spouses
        pop.sp = pop.sp.append(newsp)
        return pop
    
    def divorce(self,pop,year):
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
    def dead(self,pop,year):
        # make sure year up to date
        pop.ages(year)
        work = pop.hh.loc[:,['male','age']]
        work['year'] = year
        work = work.merge(self.mx,left_on=['year','male','age'],right_index=True,how='left')
        work['dead'] = np.random.uniform(size=len(work))<work['rate']
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
        return pop
    def educ(self,pop,year):
        pop.ages(year) 
        pop.nkids()
        # deal first with those entering school
        pop.hh.loc[pop.hh.age==5,'insch'] = True
        pop.kd.loc[pop.kd.age==5,'insch'] = True
        # now those who quit (probabilistic)
        selection = (pop.hh.insch) & (pop.hh.age>=17) & (pop.hh.age<=35)
        work = pop.hh.loc[selection,['age','male','nkids']]
        work['mother'] = (work['nkids']>0)*(work['male']!=True)
        work['father'] = (work['nkids']>0)*(work['male'])
        beta = self.par_schldone 
        work['pr'] = beta['constant']
        for a in range(18,36):
            work['pr'] += np.where(work['age']==a,beta['age'+str(a)],0.0)
        work['pr'] += beta['male']*work['male']
        work['pr'] += beta['mother']*work['mother']
        work['pr'] += beta['father']*work['father']
        work['pr'] = np.exp(work['pr'])/(1+np.exp(work['pr']))
        work['quit'] = np.random.uniform(size=len(work))<work['pr']
        work['quit'] = np.where(work['age']==35,True,work['quit'])
        quit = work[work['quit']]
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

#Description births(pbirth) dans SIMUL

#Comment obtenir les paramètres : 1) Installer regsave sur Stata (findit regsave); 2) rouler le fichier "prepare.do" puis "births.do" se trouvant dans Dropbox (CEDIA)/OLG_CAN/demo/do/; 3) Les outputs sont disponibles à Dropbox (CEDIA)/OLG_CAN/demo/params/trans_births.csv

#Sélection de l'échantillon
#	On ne garde que :
#		- Les femmes
#		- L'historique des femmes jusqu'à leurs 39 ans (les femmes n'ont plus d'enfants par la suite + les femmes n'ont pas d'enfants avant 18 ans)
#		- L'historique depuis 30 années pour éviter les effets propres aux cohortes
#		- La province du Québec

#Description des variables
#	Soit kid1-3 : la naissance de l'enfant 1 à 3 une année donnée
#	Soit : educ_ le niveau d'éducation le plus élevé 
#		Référence : N'a pas accompli ses études secondaires
#		des : = Diplôme d'études secondaires ou études PARTIELLES à l'université ou au collège communautaire
#		dec : = Diplôme d'études d'un collège communautaire
#		uni : Supérieur ou égal au baccalauréat
#	Soit dage____ l'âge des individus :
#		- référence : 18 à 24 ans
#		- dage2529 : de 25 à 29 ans
#		- dage3034 : de 30 à 34 ans
#		- dage35+  : de 35 à 39 ans

#	Soit lkidage l'âge (à partir de 1 an) du dernier enfant né : uniquement utile pour les enfants numéro 2 et numéro 3

#	Régression pour le 1er (sans lastkidage), 2nd, ..., 6ème enfant noté i
#	logit kid(i) dage2529 dage3034 dage35+ lkidage tnl pei ns nb qc man sas alb bc schldone hs college university

    
#@njit
#def pbirth(age,sp_age,male,educ,educ_sp,nkids):
#    return 0.0
        #(float64(int64,int64,int64,float64))
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

#Description pmarr et pdiv
#
#Préparation de la base :
#	On ne garde que :
#	- Les résidants du Québec
#	- L'historique depuis 30 années pour éviter les effets propres aux cohortes
#
#Variables dépendantes (dummies) :
#	- Soit m1 = 0 avant la première union (à partir de 16 ans) & m1 = 1 l'année de la première union
#	- Soit d1 = 0 entre l'année de la première union et l'année précédent la séparation & d1=1 l'année de la séparation
#	- Soit m2 = 0 entre l'année de la séparation de la première union et l'année précédent la seconde union & m1 = 1 l'année de la seconde union
#	- Soit d2 = 0 entre l'année de la seconde union et l'année précédent la séparation & d2=1 l'année de la séparation
#
#Variables indépendantes:
#
#	Âge du répondant selon le genre, sinon 0
#	- mage : âge du répondant si c'est un homme, sinon 0
#	- mage2 : âge au carré du répondant si c'est un homme, sinon 0
#	- mage3 : âge au cube du répondant si c'est un homme, sinon 0
#	- wage : âge du répondant si c'est une femme, sinon 0
#	- wage2 : âge au carré du répondant si c'est une femme, sinon 0
#	- wage3 : âge au cube du répondant si c'est une femme, sinon 0
#	- male : est égal à 1 si le répondant est un homme, sinon 0 (dummy)
#
#	Education du répondant (dummies) :
#	- Référence : N'a pas accompli ses études secondaires
#	- des : = Diplôme d'études secondaires ou études PARTIELLES à l'université ou au collège communautaire
#	- dec : = Diplôme d'études d'un collège communautaire
#	- uni : Supérieur ou égal au baccaulauréat
#
#	Enfant de moins de 18 ans (dummy) :
#	- kid : L'individu a un enfant de moins de 18 ans
#
#Usage des variables en fonction des évènements (x = variable utilisée):
#
#	var				#	d1	#	d2	#	m1	#	m2
#					#		#		#		#
#	mage			#	x	#	x	#	x	#	
#	mage2			#	x	#		#	x	#	
#	mage3			#	x	#		#		#	
#	wage			#	x	#	x	#	x	#	
#	wage2			#	x	#		#	x	#	
#	wage3			#	x	#		#		#	
#	male			#	x	#	x	#	x	#	x
#	des				#	x	#	x	#	x	#	x
#	dec				#	x	#	x	#	x	#	x
#	uni				#	x	#	x	#	x	#	x
#	kid				#	x	#		#		#	
#	constant		#	x	#	x	#	x	#	x
#
#Régressions logistiques : 
#logit m1 mage mage2 wage wage2 des dec uni
#logit d1 mage mage2 mage3 wage wage2 wage3 des dec educ_4 uni
#logit m2 male des dec uni
#logit d2 mage wage des dec uni (On applique le Logit seulement entre 25 et 54 ans)

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

#Description mortality(pdead) dans SIMUL

#Comment obtenir les paramètres : Les outputs sont disponibles à Dropbox (CEDIA)/OLG_CAN/demo/params/. Les hypothèses low, medium et high de Statcan sont disponibles : trans_mortality_low.csv, trans_mortality_medium.csv et trans_mortality_high.csv

#Etapes de préparation et de calcul pour obtenir les outputs trans_mortality_low.csv, trans_mortality_medium.csv et trans_mortality_high.csv :
#1) On utilise comme inputs les quotients de mortalité de Statcan par âge, genre, année et province disponibles entre 2013-2014 et 2062-2063. Les fichiers sont localisés à : Dropbox (CEDIA)/OLG_CAN/demo/raw/census/Quotients perspectifs de mortalite 2013-14 a 2062-63.xlsx
#2) A partir du fichier xlsx, on créé trois fichiers .csv en fonction des 3 hypothèses de Statcan : quotients-low, quotients-medium, quotients-high (pour plus de facilité on a supprimé à la main les 3 premières lignes du fichier xlsx & on a remplacé les séparateurs "," par des ".")
#3) Dans le do file :
#	- on créé une variable d'année calendaire "year" de 2013 à 2062 à partir des données qui sont à cheval sur deux années. On étend les quotients de mortalité de 2010 à 2012 (égaux à ceux de 2013) et de 2063 à 2200 (égaux à ceux de 2062).
#	- on ne conserve que les observations pour le Québec
#	- on créé une variable de genre "male" égale à 1 pour les hommes et égale à 0 pour les femmes.
#	- on créé une variable de taux de mortalité par âge de la variable "tx0" jusqu'à la variable "tx110".
#	- précision : les données initialement en quotients de mortalité sont transformés en taux de mortalité.


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

#Description de la transition de fin d'études et du niveau d'études
#
#Préparation de la base :
#	On ne garde que :
#	- Les résidants du Québec
#	- L'historique depuis 30 années pour éviter les effets propres aux cohortes
#
#Description des variables pour la transition de fin des études :
#	- "schldone"=1 si les études sont terminées et =0 si elles sont toujours en cours.
#	- male : est égal à 1 si le répondant est un homme, sinon 0 (dummy)
#	- mother=1 si l'individu est une mère, 0 sinon
#	- father=1 si l'individu est un père, 0 sinon
#	- agex=1 si l'individu a x ans, avec x = 18, ..., 35
#		L'âge de référence est 18 ans 
#
#Description des variables pour attribuer le niveau d'éducation atteind :
#	Soit "educ4" les niveaux d'éducation :
#		less_than_des=1 si l'individu n'a pas accompli ses études secondaires 
#		Référence : = Diplôme d'études secondaires ou études PARTIELLES à l'université ou au collège communautaire
#		dec : = Diplôme d'études d'un collège communautaire
#		uni : Supérieur ou égal au baccalauréat
# 
#	Soit les variables indépendantes :
#	- male : est égal à 1 si le répondant est un homme, sinon 0 (dummy)
#	- mother=1 si l'individu est une mère, 0 sinon
#	- father=1 si l'individu est un père, 0 sinon
#	- agex=1 si l'individu a x ans, avec x = 18, ..., 35
#		L'âge de référence est 18 ans 
#
#Régressions :
#logit schldone male mother father age*
#mlogit educ4 male mother father age*  if(schldone==1), base(2)

@njit 
def pdes(age,male):
    return 0.0
@njit 
def pdec(age,male):
    return 0.0
@njit 
def puni(age,male):
    return 0.0