.. _transition_models:

Modèles de transition
=====================

Naissances
----------

Modèle économétrique
^^^^^^^^^^^^^^^^^^^^
Pour chaque rang de naissance *k=1,2,3*  la probabilité d'avoir un enfant est estimée à l'aide d'un modèle logistique incluant trois groupes de variables explicatives liées à l'âge, au niveau d'éducation et à l'âge du dernier enfant, le cas échéant.

.. math:: \mu_{i,t,k} = \mu_{0,k} + \mu_{1,k} age_{i,t} + \mu_{2,k} edu_{i,t} + \mu_{3,k} lastkidage_{i,t}

.. math:: \Pr(b_{i,t}=1|\mu_{i,t,k}) = \frac{\exp(\mu_{i,t,k})}{1+\exp(\mu_{i,t,k})}

Données et échantillon
^^^^^^^^^^^^^^^^^^^^^^
Les effets marginaux sont calculés à partir des vagues 2006 et 2011 de `l'Enquête Sociale Générale (ESG)  <https://www150.statcan.gc.ca/n1/pub/89f0115x/89f0115x2013001-fra.htm>`_ réalisée par Statistique Canada auprès des ménages.

L'échantillon utilisé pour calculer les 3 régressions logistiques des transitions de naissance est défini en suivant plusieurs étapes :

    1. Les données des vagues 2006 et 2011 de l'Enquête sociale générale (ESG) sont regroupées (*pooled*) dans une base unique.
    2. On restreint l'échantillon aux données de la province du Québec (variable *prv*).
    3. On créé un fichier de pseudo panel des répondants qui recense l'historique des transitions de naissances 1, 2 et 3 
       (calcul des naissances pour chaque année à partir des variables *agechdc1*, *agechdc2* et *agechdc3* correspondant à l'âge des enfants d'ordre 1,2 et 3).
    4. On conserve seulement l'historique des transitions du pseudo panel depuis 30 années afin d'éviter les effets des cohortes les plus anciennes (*2006-30* pour la première vague ESG et *2011-30* pour la seconde vague).
    5. On restreint l'échantillon aux femmes âgées de 18 à 39 ans inclus.

Variables dépendantes et variables explicatives
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Les variables dépendantes pour les régressions 1, 2 et 3 sont des variables indicatrices (*dummies*) égales à 1 l'année de naissance de l'enfant d'ordre *k=1,2,3* et elles sont égales 
à 0 depuis l'année de naissance du dernier enfant (pour les naissances d'ordre 2 et 3) et depuis 18 ans pour l'aîné des enfants (naissance d'ordre 1).

**Variables explicatives d'âge (variables indicatrices) :**

    - *dage1824* (référence) : la femme a entre 18 et 24 ans.
    - *dage2529* : la femme a entre 25 et 29 ans.
    - *dage3034* : la femme a entre 30 et 34 ans.
    - *dage35+* : la femme a entre 35 et 39 ans.

**Variables explicatives d'éducation (variables indicatrices) :**

    - *insch* : la femme n'a pas terminé ses études.
    - *inf* (référence) : la femme a terminé ses études, mais n'a pas accompli ses études secondaires.
    - *des* : la femme a terminé ses études & a un diplôme d'études secondaires ou un diplôme d'études partielles à l'université ou au collège communautaire.
    - *dec* : la femme a terminé ses études & a un diplôme d'études d'un collège communautaire.
    - *uni* : la femme a terminé ses études & a un diplôme supérieur ou égal au baccaulauréat.

**Variable du dernier enfant :**

    - *lkidage* : âge du dernier enfant né. Cette variable est uniquement utilisée pour les naissances d'ordre 2 et 3.

Résultats de la régression logistique et implémentation dans le modèle démographique
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Les résultats des régressions logistiques sont présentés dans le tableau suivant : 

.. csv-table:: Logit - Coefficients des transitions de naissances
   :widths: 20 20 20 20
   :header-rows: 1
   :align: center
   :file: csv_files/trans_births.csv

L'implémentation dans le modèle démographique est réalisée par un tirage uniforme, indépendant par dominant, et une naissance survient quand ce tirage est inférieur à la probabilité logistique prédite.

Dans le modèle de simulation démographique, les personnes à risque pour cette transition sont les dominants en union de plus de 18 ans et dont la femme à moins de 45 ans. Il faut préciser que la régression logistique est estimée jusque 39 ans (34< *dage35+* <40), mais que les effets marginaux de la variable *dage35+* sont appliquées aux conjointes âgées jusque 45 ans dans le modèle de microsimulation démographique.

Il faut préciser que les effets marginaux obtenus pour le Logit appliqué au 3ème enfant *kid3* est utilisé dans la simulation démographique pour calculer l'occurence de la naissance du 3ème enfant, mais également des enfants suivants.

Fin des études et niveau d'études associé
-----------------------------------------

Tous les enfants débutent leurs études l'année de leurs 5 ans. La présente transition calcule la probabilité de finir ses études ainsi que le niveau d'études correspondant.

Modèle économétrique
^^^^^^^^^^^^^^^^^^^^

Deux régressions logistiques sont appliquées pour 1) calculer la probabilité de finir ses études ; 2) attribuer un niveau d'études aux individus qui ont accompli leurs études. Une régression logistique ordinaire est appliquée pour calculer la probabilité de finir ses études et un modèle logistique multinomial est utilisé pour définir le niveau d'étude correspondant.

1) probabilité *f* d'un individu *i* de finir ses études l'année *t* : 

.. math:: \mu_{i,t} = \mu_{0} + \mu_{1} age_{i,t} + \mu_{2} male_{i,t} + \mu_{3} father_{i,t} + \mu_{4} mother_{i,t}

.. math:: \Pr(f_{i,t}=1|\mu_{i,t}) = \frac{\exp(\mu_{i,t})}{1+\exp(\mu_{i,t})}

2) pour chaque niveau d'éducation *e = 1 (inf), 2 (des) [référence], 3 (dec), 4 (uni)* atteint par un individu *i* l'année d'accomplissement des études en *t* : 

.. math:: \mu e_{i,t} = \mu_{0} + \mu_{1} age_{i,t} + \mu_{2} male_{i,t} + \mu_{3} father_{i,t} + \mu_{4} mother_{i,t}

.. math:: \Pr(e_{i,t}=1|\mu1_{i,t}) = \frac{\exp(\mu1_{i,t})}{1+\exp(\mu1_{i,t})+\exp(\mu3_{i,t})+\exp(\mu4_{i,t})}

.. math:: \Pr(e_{i,t}=2|\mu2_{i,t}) = \frac{1}{1+\exp(\mu1_{i,t})+\exp(\mu3_{i,t})+\exp(\mu4_{i,t})}

.. math:: \Pr(e_{i,t}=3|\mu3_{i,t}) = \frac{\exp(\mu3_{i,t})}{1+\exp(\mu1_{i,t})+\exp(\mu3_{i,t})+\exp(\mu4_{i,t})}

.. math:: \Pr(e_{i,t}=4|\mu4_{i,t}) = \frac{\exp(\mu4_{i,t})}{1+\exp(\mu1_{i,t})+\exp(\mu3_{i,t})+\exp(\mu4_{i,t})}

Données et échantillon
^^^^^^^^^^^^^^^^^^^^^^
Les régressions logistiques sont calculées à partir des vagues 2006 et 2011 de `l'Enquête Sociale Générale (ESG)  <https://www150.statcan.gc.ca/n1/pub/89f0115x/89f0115x2013001-fra.htm>`_ réalisée par Statistique Canada auprès des ménages.

L'échantillon utilisé pour calculer les transitions de naissance est défini en suivant plusieurs étapes :

    1) Les données des vagues 2006 et 2011 de l'Enquête sociale générale (ESG) sont regroupées (*pooled*) dans une base unique.
    2) On restreint l'échantillon aux données de la province du Québec.
    3) On créé un fichier de pseudo panel des individus répondants qui recense l'historique des transitions de fin d'études et le niveau d'études associé.
    4) On conserve seulement l'historique des transitions du pseudo panel depuis 30 années afin d'éviter les effets des cohortes les plus anciennes (*2006-30* pour la première vague ESG et *2011-30* pour la seconde vague).
    5) On restreint l'échantillon aux individus âgés de 17 à 35 ans inclus.
    6) On supprime les années qui suivent l'année d'accomplissement des études.
    7) Pour la régresion logistique multinomiale du niveau d'étude, l'échantillon est restreint à l'année d'accomplissement des études.

Variables dépendantes et variables explicatives
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La variable dépendante *schldone* définissant la probabilité de finir ses études est égale à 1 lorsque l'individu a accompli ses études et elle est égale à 0 lorsque l'individu n'a pas encore accompli ses études. Cette variable indicatrice (*dummy*) est calculée à partir de la variable *agecmplt* (âge du répondant à la fin des études) de l'ESG.

**La variable dépendante et indicatrice du niveau d'études "educ" est utilisée dans une régression logistique multinomiale. Elle inclut 4 niveaux d'éducation :**

    - *inf* : n'a pas accompli ses études secondaires.
    - *des* (référence) : a obtenu un diplôme d'études secondaires ou un diplôme d'études partielles à l'université ou au collège communautaire.
    - *dec* : a obtenu un diplôme d'études d'un collège communautaire.
    - *uni* : a obtenu un diplôme supérieur ou égal au baccaulauréat.

**Les variables explicatives et indicatrices de la fin des études "schldone" et du niveau d'études atteint sont les suivantes :**

    - *male* : égal à 1 si le répondant est un homme et égal à 0 si le répondant est une femme.
    - *father* : égal à 1 si le répondant est un homme avec des enfants, 0 sinon.
    - *mother* : égal à 1 si le répondant est une femme avec des enfants, 0 sinon.
    - *agex* : égal à 1 si l'individu a *x* ans, 0 sinon, avec *x* = 17 à 35 ans (la référence et constituée des individus âgés de 17 ans).

Résultats des régressions logistiques et implémentation dans le modèle démographique
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Les résultats des régressions logistiques sont présentés dans le tableau suivant : 

.. csv-table:: Logit - Coefficients de la transition de fin d'études (colonne 2) et d'attribution des niveaux d'études (colonne 3 à 5)
   :widths: 20 20 20 20 20
   :header-rows: 1
   :align: center
   :file: csv_files/trans_educ.csv

L'implémentation dans le modèle démographique est réalisée par un tirage uniforme, indépendant par dominant, et la fin des études et le niveau d'études associé survient quand ce tirage est inférieur à la probabilité logistique prédite. 

Dans le modèle de simulation démographique, les personnes à risque pour cette transition sont les dominants âgés de 18 à 35 ans qui sont encore en études. Les individus âgés de 35 ans ont une probabilité de finir leurs études fixée à 100%. Avant l'année de fin des études, les individus sont considérés sans éducation (aucun niveau ne leur est attribué). Le niveau d'études obtenu l'année de fin des études est attribué aux individus jusqu'à la fin de leurs vie. Aucun retour en études n'est possible après la fin des études.

Mises en couples et séparations
-------------------------------

Modèle économétrique
^^^^^^^^^^^^^^^^^^^^

Deux régressions logistiques sont appliquées pour 1) calculer la probabilité de se mettre en couple (union libre ou mariage indifféremment); 2) calculer la probabilité de se séparer. La probabilité de se mettre en couple et de se séparer dépend de variables similaires liées à l'âge du répondant, à son genre et à son niveau d'éducation. De plus, la probabilité de se séparer dépend également de la présence d'au moins un enfant âgé de moins de 18 ans.

1) probabilité *c* d'un individu *i* de se mettre en couple l'année *t* : 

.. math:: \mu_{i,t} = \mu_{0} + \mu_{1} age_{i,t} + \mu_{2} male_{i,t} + \mu_{3} educ_{i,t}

.. math:: \Pr(c_{i,t}=1|\mu_{i,t}) = \frac{\exp(\mu_{i,t})}{1+\exp(\mu_{i,t})}

2) probabilité *s* d'un individu *i* de se séparer l'année *t* : 

.. math:: \mu_{i,t} = \mu_{0} + \mu_{1} age_{i,t} + \mu_{2} male_{i,t} + \mu_{3} educ_{i,t} + \mu_{4} kid_{i,t}

.. math:: \Pr(s_{i,t}=1|\mu_{i,t}) = \frac{\exp(\mu_{i,t})}{1+\exp(\mu_{i,t})}

Données et échantillon
^^^^^^^^^^^^^^^^^^^^^^
Les modèles logistiques sont calculés à partir des vagues 2006 et 2011 de `l'Enquête Sociale Générale (ESG)  <https://www150.statcan.gc.ca/n1/pub/89f0115x/89f0115x2013001-fra.htm>`_ réalisée par Statistique Canada auprès des ménages.

L'échantillon utilisé pour calculer les transitions de naissance est défini en suivant plusieurs étapes :

    1) Les données des vagues 2006 et 2011 de l'Enquête sociale générale (ESG) sont regroupées (*pooled*) dans une base unique.
    2) On restreint l'échantillon aux données de la province du Québec (variable *prv*).
    3) On créé un fichier de pseudo panel des individus répondants qui recense l'historique des transitions d'unions et de séparations d'ordre 1 à 4 (jusqu'à 4 unions et séparations sont possibles tout au long de la vie).
    4) On conserve seulement l'historique des transitions du pseudo panel depuis 30 années afin d'éviter les effets des cohortes les plus anciennes (*2006-30* pour la première vague ESG et *2011-30* pour la seconde vague).

Variables dépendantes et variables explicatives
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pour calculer la transition de mise en union, la variable dépendante est égale à 0 lorsque l'individu est célibataire et la variable dépendante est égale à 1 l'année de la mise en couple. Symétriquement, pour le calcul de la transition de séparation, la variable dépendante est égale à 0 lorsque l'individu est en couple et la variable dépendante est égale à 1 l'année de la séparation. Il faut préciser que le fait de devenir veuf n'est pas considéré comme une transition de séparation dans le modèle logistique.

**1) Variables explicatives des transitions de mise en couple :**

**Genre (variable indicatrice) :**

    - *male* : égal à 1 si le répondant est un homme et égal à 0 si le répondant est une femme.

**Âge (variables indicatrices) :**

    - *age1619* : le répondant à entre 16 et 19 ans.
    - *age2024* : le répondant à entre 20 et 24 ans.
    - *age2529* : le répondant à entre 25 et 29 ans.
    - *age3034* (référence) : le répondant à entre 30 et 34 ans.
    - *age3539* : le répondant à entre 35 et 39 ans.
    - *age4044* : le répondant à entre 40 et 44 ans.
    - *age4549* : le répondant à entre 45 et 49 ans.
    - *age5054* : le répondant à entre 50 et 54 ans.
    - *age5559* : le répondant à entre 55 et 59 ans.
    - *age6065* : le répondant à entre 60 et 65 ans.

**Education (variables indicatrices) :**

    - *insch* : le répondant n'a pas terminé ses études.
    - *inf* (référence) : le répondant a terminé ses études mais n'a pas accompli ses études secondaires.
    - *des* : le répondant a terminé ses études & a un diplôme d'études secondaires ou un diplôme d'études partielles à l'université ou au collège communautaire.
    - *dec* : le répondant a terminé ses études & a un diplôme d'études d'un collège communautaire.
    - *uni* : le répondant a terminé ses études & a un diplôme supérieur ou égal au baccaulauréat.
    
**2) Variable explicative des transitions de séparation :**

**Genre (variable indicatrice) :**

    - *male* : le répondant est un homme et égal à 0 si le répondant est une femme.

**Âge :**

    - *mage* : âge du répondant si c'est un homme, sinon 0.
    - *mage2* : âge au carré du répondant si c'est un homme, sinon 0.
    - *mage3* : âge au cube du répondant si c'est un homme, sinon 0.
    - *wage* : âge du répondant si c'est une femme, sinon 0.
    - *wage2* : âge au carré du répondant si c'est une femme, sinon 0.
    - *wage3* : âge au cube du répondant si c'est une femme, sinon 0.

**Education (variables indicatrices) :**

    - *insch* : le répondant n'a pas terminé ses études.
    - *inf* (référence) : le répondant a terminé ses études mais n'a pas accompli ses études secondaires.
    - *des* : le répondant a terminé ses études & a un diplôme d'études secondaires ou un diplôme d'études partielles à l'université ou au collège communautaire.
    - *dec* : le répondant a terminé ses études & a un diplôme d'études d'un collège communautaire.
    - *uni* : le répondant a terminé ses études & a un diplôme supérieur ou égal au baccaulauréat.
    
**Enfants (variable indicatrice) :**

    - *kid* : égal à 1 si le répondant a un enfant de moins de 18 ans, 0 sinon. 
    
Cette variable contrôle la présence d'enfants mineurs, potentiellement résidants au domicile parental ou bien à la charge de leurs parents. La présence d'enfants majeurs ne sont pas pris en compte car ils ne sont potentiellement plus à la charge de leurs parents.  

Résultats des régressions logistiques et implémentation dans le modèle démographique
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Les résultats du modèle logistique de mise en couple sont présentés dans le tableau suivant :     

.. csv-table:: Logit - Coefficients des transitions de mise en couple
   :widths: 20 20
   :header-rows: 1
   :align: center
   :file: csv_files/trans_unions.csv

Les résultats du modèle logistique de séparations sont présentés dans le tableau suivant :     
 
.. csv-table:: Logit - Coefficients des transitions de séparations
   :widths: 20 20
   :header-rows: 1
   :align: center
   :file: csv_files/trans_divorces.csv

L'implémentation de la transition de mise en couple et de séparation dans le modèle démographique est réalisée par un tirage uniforme, indépendant par dominant, et une mise en couple ou une séparation survient quand ce tirage est inférieur à la probabilité logistique prédite. 

Pour le dominant *D1* nouvellement en couple, les caractéristiques du nouveau conjoint *C1* sont attribuées en tirant aléatoirement un autre individu dominant *D2* ayant le même genre et le même niveau d'éducation que *D1*. De plus, On restreint le bassin de tirage aux dominants *D2* qui ont un écart d'âge avec leur conjoint *C2* qui est inférieur à 5 ans (en valeur absolue). Si pour un dominant *D1*, aucun conjoint n'est identifié en appliquant cette restriction d'écart d'âge, alors on réalise un second tirage dans le bassin des dominants *D2* qui ont le même genre et le même niveau d'éducation que *D1*, et qui ont un écart d'âge avec leur conjoint *C2* inférieur à 20 ans (en valeur absolue). Les caractéristiques du conjoint *C2* sont alors attribuées au nouveau conjoint *C1* du dominant *D1* nouvellement en couple (âge, genre et éducation). Il faut également préciser que dans la version actuelle de SimGen, le nouveau conjoint *C1* qui est attribué au dominant *D1* est systématiquement du sexe opposé. De futures versions du modèle pourront intégrer une représentation plus diversifiée des unions matrimoniales.

Décès
-----

Chaque année *t*, un individu d'âge *a* et de genre *g* a une probabilité *P(t,a,g)* de décéder. Cette probabilité, définie comme un taux de mortalité, est calculé à partir des quotients perspectifs de mortalité selon l'âge et le sexe estimés par Statistique Canada entre 2013-2014 et 2062-2063 (de juillet-juin) pour les provinces et territoires. Le `rapport technique  <https://www150.statcan.gc.ca/n1/pub/91-620-x/91-620-x2014001-fra.pdf>`_ de Statistique Canada présente la méthodologie et les hypothèses de ces quotients perspectifs.

L'âge, le genre et la cohorte de naissance sont donc les uniques déterminants de l'espérance de vie des individus. Notons également que les immigrants et les natifs ont des probabilités équivalentes de décès en fonction de leur âge, genre et cohorte.

Migrations
----------

Les taux prospectifs d'immigration et d'émigration sont respectivement égaux à 5,35‰ et 1,16‰. Ces taux sont identiques pour toutes les années simulées. Ils sont calculés à partir du nombre de nouveaux immigrants (44 856 personnes) et du nombre de nouveaux émigrants (9 741 personnes) enregistrés au Québec pour la période 2018-2019 par Statistique Canada, ainsi que de la population Québecoise au 1er juillet 2018 calculée par Statistique Canada (8 387 632 personnes).

- Le nombre d'immigrants et le nombre d'émigrants en 2018-2019 sont issus du `tableau 17-10-0014-01 "Estimations des composantes de la migration internationale, par âge et sexe, annuelles"  <https://www150.statcan.gc.ca/t1/tbl1/fr/tv.action?pid=1710001401>`_.
- la population Québecoise au 1er juillet 2018 issue du `tableau 17-10-0005-01 "Estimations de la population au 1er juillet, par âge et sexe"  <https://www150.statcan.gc.ca/t1/tbl1/fr/tv.action?pid=1710000501>`_.

Les caractéristiques socio-économiques et démographiques des nouveaux immigrants sont attribuées en fonction des immigrants récents issus de la Base de données et Modèle de simulation de politiques sociales de Statistique Canada (BD/MSPS) pour l'année 2017. Chaque année t, on tire aléatoirement 0,0535*Population(t) de nouveaux immigrants parmis ceux de l'année 2017. Les caractéristiques socio-économiques et démographiques des nouveaux immigrants sont alors celles des immigrants tirés de BD/MSPS 2017 : l'âge, le genre, le niveau d'éducation, la présence de conjoint et le nombre d'enfants.

Les caractéristiques des émigrants dépendent uniquement de l'âge. A chaque âge donné, la probabilité d'émigrer est égale pour toutes les personnes dominantes. Les émigrants d'un âge donné sont tirés de manière aléatoire. De plus, on considère que le(la) conjoint(e) du dominant ainsi que tous ses enfants âgés de moins de 18 ans émigrent avec la personne dominante. Le taux d'émigration par âge est calculé à partir du nombre d'émigrants par classes d'âge en 2018-2019 du `tableau 17-10-0014-01 "Estimations des composantes de la migration internationale, par âge et sexe, annuelles"  <https://www150.statcan.gc.ca/t1/tbl1/fr/tv.action?pid=1710001401>`_ et de la population Québecoise par classes d'âge au 1er juillet 2018 du `tableau 17-10-0005-01 "Estimations de la population au 1er juillet, par âge et sexe"  <https://www150.statcan.gc.ca/t1/tbl1/fr/tv.action?pid=1710000501>`_. Les taux d'émigrations par classes d'âge sont les suivants :

.. csv-table:: 
 :header: "Classe d'âge", "Taux d'émigration (‰)"
 :widths: 100, 100
 :align: center

 "15 à 19 ans", "0,53"
 "20 à 24 ans", "1,16"
 "25 à 29 ans", "2,29"
 "30 à 34 ans", "2,64"
 "35 à 39 ans", "2,11"
 "40 à 44 ans", "1,55"
 "45 à 49 ans", "1,19"
 "50 à 54 ans", "0,81"
 "55 à 59 ans", "0,55"
 "60 à 64 ans", "0,42"
 "65 à 69 ans", "0,39"
 "70 à 74 ans", "0,28"
 "75 à 79 ans", "0,31"
 "80 à 84 ans", "0,33"
 "85 à 89 ans", "0,31"
 "90 ans et plus", "0,36"










