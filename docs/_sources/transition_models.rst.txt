.. _transition_models:

Modèles de transition
=====================

Naissances
----------

Modèle économétrique
^^^^^^^^^^^^^^^^^^^^
Pour chaque rang de naissance *k=1,2,3*, la probabilité d'avoir un enfant est estimée à l'aide d'un modèle logistique incluant trois groupes de variables explicatives liées à l'âge, au niveau de scolarité et à l'âge du dernier enfant, le cas échéant.

.. math:: \mu_{i,t,k} = \mu_{0,k} + \mu_{1,k} age_{i,t} + \mu_{2,k} edu_{i,t} + \mu_{3,k} lastkidage_{i,t}

.. math:: \Pr(b_{i,t}=1) = \frac{\exp(\mu_{i,t,k})}{1+\exp(\mu_{i,t,k})}

Données et échantillon
^^^^^^^^^^^^^^^^^^^^^^
Les effets marginaux sont calculés à partir des vagues 2006 et 2011 de `l'Enquête sociale générale (ESG)  <https://www150.statcan.gc.ca/n1/pub/89f0115x/89f0115x2013001-fra.htm>`_ menée auprès des ménages par Statistique Canada.

L'échantillon utilisé pour calculer les 3 régressions logistiques des transitions de naissance est défini en suivant plusieurs étapes:

    1. Les données des vagues 2006 et 2011 de l'ESG sont regroupées (*pooled*) dans une base unique.
    2. On restreint l'échantillon aux données du Québec (variable *prv*).
    3. On créé un fichier de pseudo panel des répondants qui recense l'historique des transitions de naissances 1, 2 et 3 (calcul des naissances pour chaque année à partir des variables *agechdc1*, *agechdc2* et *agechdc3* correspondant à l'âge des enfants d'ordre 1, 2 et 3).
    4. On conserve seulement l'historique des transitions du pseudo panel depuis 30 années afin d'éviter les effets des cohortes les plus anciennes (*2006-30* pour la première vague ESG et *2011-30* pour la seconde vague).
    5. On restreint l'échantillon aux femmes âgées de 18 à 44 ans inclusivement.

Variables dépendantes et variables explicatives
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Les variables dépendantes pour les régressions 1, 2 et 3 sont des variables indicatrices (*dummies*), égales à 1 l'année de naissance de l'enfant d'ordre *k=1,2,3* et égales à 0 depuis l'année de naissance du dernier enfant (pour les naissances d'ordre 2 et 3) et depuis 18 ans pour l'aîné des enfants (naissance d'ordre 1).

**Variables explicatives d'âge (variables indicatrices):**

    - *dage1824* (référence) : la femme a entre 18 et 24 ans.
    - *dage2529* : la femme a entre 25 et 29 ans.
    - *dage3034* : la femme a entre 30 et 34 ans.
    - *dage3539* : la femme a entre 35 et 39 ans.
    - *dage40p* : la femme a entre 40 et 44 ans.

**Variables explicatives d'éducation (variables indicatrices):**

    - *insch* : la femme n'a pas terminé ses études.
    - *inf* (référence) : la femme a terminé ses études, mais n'a pas complété ses études secondaires.
    - *des* : la femme a terminé ses études et a un diplôme d'études secondaires ou des études partielles à l'université ou au cégep.
    - *dec* : la femme a terminé ses études et a un diplôme d'études collégiales.
    - *uni* : la femme a terminé ses études et a un diplôme égal ou supérieur au baccalauréat.

**Variable du dernier enfant :**

    - *lkidage* : âge du dernier enfant né. Cette variable est uniquement utilisée pour les naissances d'ordre 2 et 3.

Résultats de la régression logistique et mise en œuvre dans le modèle démographique
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Les résultats des régressions logistiques sont présentés dans le tableau suivant:

.. csv-table:: Logit - Coefficients des transitions de naissances
   :widths: 20 20 20 20
   :header-rows: 1
   :align: center
   :file: csv_files/trans_births.csv

L'implémentation dans le modèle démographique est réalisée par un tirage uniforme, indépendant par individu dominant, et une naissance survient quand le résultat de ce tirage est inférieur à la probabilité logistique prédite.

Dans le modèle de simulation démographique, les personnes à risque pour cette transition sont les femmes en couple (qu'elles soient enregistrées comme l'individu dominant ou la conjointe dans la BDSPS) âgées de 18 ans à 44 ans inclusivement.

Il faut préciser que les effets marginaux obtenus pour le logit appliqué au 3e enfant (*kid3*) est utilisé dans la simulation démographique pour calculer l'occurrence de la naissance du 3e enfant, mais également des enfants suivants.

Fin des études et niveau de scolarité associé
---------------------------------------------

Tous les enfants débutent leurs études l'année de leurs 5 ans. La présente transition calcule la probabilité de finir ses études ainsi que le niveau de scolarité correspondant.

Modèle économétrique
^^^^^^^^^^^^^^^^^^^^

Deux régressions logistiques sont réalisées pour 1) calculer la probabilité de finir ses études ; 2) attribuer un niveau de scolarité aux individus qui ont complété leurs études. Une régression logistique ordinaire est appliquée pour calculer la probabilité de finir ses études et un modèle logistique multinomial est utilisé pour définir le niveau de scolarité correspondant.

1) probabilité d'un individu *i* de finir ses études *f* l'année *t* :

.. math:: \mu_{i,t} = \mu_{0} + \mu_{1} age_{i,t} + \mu_{2} male_{i,t} + \mu_{3} father_{i,t} + \mu_{4} mother_{i,t}

.. math:: \Pr(f_{i,t}=1) = \frac{\exp(\mu_{i,t})}{1+\exp(\mu_{i,t})}

2) pour chaque niveau d'éducation *e = 1 (inf), 2 (des) [référence], 3 (dec), 4 (uni)* atteint par un individu *i* l'année de terminaison des études en *t* :

.. math:: \mu_{e(i,t)} = \mu_{0} + \mu_{i} age_{i,t} + \mu_{j} male_{i,t} + \mu_{k} father_{i,t} + \mu_{l} mother_{i,t}

.. math:: \Pr(e_{i,t}=1) = \frac{\exp(\mu_{1(i,t)})}{1+\exp(\mu_{1(i,t)})+\exp(\mu_{3(i,t)})+\exp(\mu_{4(i,t)})}

.. math:: \Pr(e_{i,t}=2) = \frac{1}{1+\exp(\mu_{1(i,t)})+\exp(\mu_{3(i,t)})+\exp(\mu_{4(i,t)})}

.. math:: \Pr(e_{i,t}=3) = \frac{\exp(\mu_{3(i,t)})}{1+\exp(\mu_{1(i,t)})+\exp(\mu_{3(i,t)})+\exp(\mu_{4(i,t)})}

.. math:: \Pr(e_{i,t}=4) = \frac{\exp(\mu_{4(i,t)})}{1+\exp(\mu_{1(i,t)})+\exp(\mu_{3(i,t)})+\exp(\mu_{4(i,t)})}

Données et échantillon
^^^^^^^^^^^^^^^^^^^^^^
Les régressions logistiques sont réalisées à l'aide des vagues 2006 et 2011 de `l'Enquête sociale générale (ESG)  <https://www150.statcan.gc.ca/n1/pub/89f0115x/89f0115x2013001-fra.htm>`_ menée auprès des ménages par Statistique Canada.

L'échantillon utilisé pour calculer les transitions d'éducation est défini en suivant plusieurs étapes :

    1) Les données des vagues 2006 et 2011 de l'ESG sont regroupées (*pooled*) dans une base unique.
    2) On restreint l'échantillon aux données du Québec (variable *prv*).
    3) On créé un fichier de pseudo panel des individus répondants qui recense l'historique des transitions de fin d'études et le niveau de scolarité associé.
    4) On conserve seulement l'historique des transitions du pseudo panel depuis 30 années afin d'éviter les effets des cohortes les plus anciennes (*2006-30* pour la première vague ESG et *2011-30* pour la seconde vague).
    5) On restreint l'échantillon aux individus âgés de 17 à 35 ans inclusivement.
    6) On supprime les années qui suivent l'année de terminaison des études.
    7) Pour la régression logistique multinomiale du niveau de scolarité, l'échantillon est restreint à l'année de terminaison des études.

Variables dépendantes et variables explicatives
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La variable dépendante *schldone* définissant la probabilité de finir ses études est égale à 1 lorsque l'individu a terminé ses études et elle est égale à 0 lorsque l'individu n'a pas encore terminé ses études. Cette variable indicatrice (*dummy*) est calculée à partir de la variable *agecmplt* (âge du répondant à la fin des études) de l'ESG.

**La variable dépendante et indicatrice du niveau de scolarité "educ" est utilisée dans une régression logistique multinomiale. Elle inclut 4 niveaux de scolarité:**

    - *inf* : n'a pas terminé ses études secondaires.
    - *des* (référence) : a obtenu un diplôme d'études secondaires ou des études partielles à l'université ou au cégep.
    - *dec* : a obtenu un diplôme d'études collégiales.
    - *uni* : a obtenu un diplôme égal ou supérieur au baccalauréat.

**Les variables explicatives et indicatrices de la fin des études "schldone" et du niveau de scolarité atteint sont les suivantes :**

    - *male* : égal à 1 si le répondant est un homme et égal à 0 si le répondant est une femme.
    - *father* : égal à 1 si le répondant est un homme avec des enfants, 0 sinon.
    - *mother* : égal à 1 si le répondant est une femme avec des enfants, 0 sinon.
    - *agex* : égal à 1 si l'individu a *x* ans, 0 sinon, avec *x* = 17 à 35 ans (la catégorie de référence est constituée des individus âgés de 17 ans).

Résultats des régressions logistiques et mise en œuvre dans le modèle démographique
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Les résultats des régressions logistiques sont présentés dans le tableau suivant :

.. csv-table:: Logit - Coefficients de la transition de fin d'études (colonne 2) et d'attribution des niveaux d'études (colonne 3 à 5)
   :widths: 20 20 20 20 20
   :header-rows: 1
   :align: center
   :file: csv_files/trans_educ.csv

La mise en œuvre dans le modèle démographique est réalisée à l'aide d'un tirage uniforme, indépendant par individu dominant, et la fin des études et le niveau de scolarité associé sont déterminés lorsque le résultat de ce tirage est inférieur à la probabilité logistique prédite.

Dans le modèle de simulation démographique, les personnes à risque pour cette transition sont les individus dominants âgés de 18 à 35 ans qui sont encore aux études. Les individus âgés de 35 ans ont une probabilité de terminé leurs études fixée à 100%. Avant l'année de fin des études, les individus sont considérés sans éducation (aucun niveau ne leur est attribué). Le niveau de scolarité obtenu l'année de fin des études est attribué aux individus jusqu'à la fin de leur vie. Aucun retour aux études n'est possible après la fin des études.

Mises en couple et séparations
------------------------------

Modèle économétrique
^^^^^^^^^^^^^^^^^^^^

Deux régressions logistiques sont réalisées pour 1) calculer la probabilité d'entrer dans une union (union libre ou mariage, indistinctement); 2) calculer la probabilité de se séparer. La probabilité d'entrer en union et de se séparer dépend de variables similaires liées à l'âge du répondant, à son genre et à son niveau de scolarité. De plus, la probabilité de se séparer dépend également de la présence d'au moins un enfant âgé de moins de 18 ans.

1) probabilité *c* d'un individu *i* de se mettre en couple l'année *t* :

.. math:: \mu_{i,t} = \mu_{0} + \mu_{1} age_{i,t} + \mu_{2} male_{i,t} + \mu_{3} educ_{i,t}

.. math:: \Pr(c_{i,t}=1) = \frac{\exp(\mu_{i,t})}{1+\exp(\mu_{i,t})}

2) probabilité *s* d'un individu *i* de se séparer l'année *t* :

.. math:: \mu_{i,t} = \mu_{0} + \mu_{1} age_{i,t} + \mu_{2} male_{i,t} + \mu_{3} educ_{i,t} + \mu_{4} kid_{i,t}

.. math:: \Pr(s_{i,t}=1) = \frac{\exp(\mu_{i,t})}{1+\exp(\mu_{i,t})}

Données et échantillon
^^^^^^^^^^^^^^^^^^^^^^
Les modèles logistiques sont estimés à partir des vagues 2006 et 2011 de `l'Enquête sociale générale (ESG)  <https://www150.statcan.gc.ca/n1/pub/89f0115x/89f0115x2013001-fra.htm>`_ réalisée auprès des ménages par Statistique Canada.

L'échantillon utilisé pour calculer les transitions maritales est défini en suivant plusieurs étapes:

    1) Les données des vagues 2006 et 2011 de l'ESG sont regroupées (*pooled*) dans une base unique.
    2) On restreint l'échantillon aux données de la province du Québec (variable *prv*).
    3) On créé un fichier de pseudo panel des individus répondants qui recense l'historique des transitions d'unions et de séparations d'ordre 1 à 4 (jusqu'à 4 unions et séparations sont possibles tout au long de la vie).
    4) On conserve seulement l'historique des transitions du pseudo panel depuis 30 années afin d'éviter les effets des cohortes les plus anciennes (*2006-30* pour la première vague ESG et *2011-30* pour la seconde vague).

Variables dépendantes et variables explicatives
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pour calculer la transition de mise en union, la variable dépendante est égale à 0 lorsque l'individu est célibataire et la variable dépendante est égale à 1 à partir de l'année de la mise en couple. Symétriquement, pour le calcul de la transition de séparation, la variable dépendante est égale à 0 lorsque l'individu est en couple et la variable dépendante est égale à 1 à partir de l'année de la séparation. Il faut préciser que le fait de devenir veuf n'est pas considéré comme une transition de séparation dans le modèle logistique.

**1) Variables explicatives des transitions de mise en couple :**

**Genre (variable indicatrice) :**

    - *male* : égal à 1 si le répondant est un homme et égal à 0 si le répondant est une femme.

**Âge (variables indicatrices) :**

    - *age1619* : le répondant a entre 16 et 19 ans.
    - *age2024* : le répondant a entre 20 et 24 ans.
    - *age2529* : le répondant a entre 25 et 29 ans.
    - *age3034* (référence) : le répondant a entre 30 et 34 ans.
    - *age3539* : le répondant a entre 35 et 39 ans.
    - *age4044* : le répondant a entre 40 et 44 ans.
    - *age4549* : le répondant a entre 45 et 49 ans.
    - *age5054* : le répondant a entre 50 et 54 ans.
    - *age5559* : le répondant a entre 55 et 59 ans.
    - *age6065* : le répondant a entre 60 et 65 ans.

**Éducation (variables indicatrices) :**

    - *insch* : le répondant n'a pas encore terminé ses études.
    - *inf* (référence) : le répondant a terminé ses études mais n'a pas complété ses études secondaires.
    - *des* : le répondant a terminé ses études et a un diplôme d'études secondaires ou des études partielles à l'université ou au cégep.
    - *dec* : le répondant a terminé ses études et a un diplôme d'études collégiales.
    - *uni* : le répondant a terminé ses études et a un diplôme égal ou supérieur au baccalauréat.

**2) Variables explicatives des transitions de séparation :**

**Genre (variable indicatrice) :**

    - *male* : le répondant est un homme et égal à 0 si le répondant est une femme.

**Âge :**

    - *mage* : âge du répondant si c'est un homme, sinon 0.
    - *mage2* : âge au carré du répondant si c'est un homme, sinon 0.
    - *mage3* : âge au cube du répondant si c'est un homme, sinon 0.
    - *wage* : âge du répondant si c'est une femme, sinon 0.
    - *wage2* : âge au carré du répondant si c'est une femme, sinon 0.
    - *wage3* : âge au cube du répondant si c'est une femme, sinon 0.

**Éducation (variables indicatrices) :**

    - *insch* : le répondant n'a pas encore terminé ses études.
    - *inf* (référence) : le répondant a terminé ses études mais n'a pas complété ses études secondaires.
    - *des* : le répondant a terminé ses études et a un diplôme d'études secondaires ou des études partielles à l'université ou au cégep.
    - *dec* : le répondant a terminé ses études et a un diplôme d'études collégiales.
    - *uni* : le répondant a terminé ses études et a un diplôme égal ou supérieur au baccalauréat.

**Enfants (variable indicatrice) :**

    - *kid* : égal à 1 si le répondant a au moins un enfant de moins de 18 ans, 0 sinon.

Cette variable contrôle pour la présence d'enfants mineurs, potentiellement résidants au domicile parental ou bien à la charge de leurs parents. La présence d'enfants majeurs n'est' pas prise en compte car ceux-ci ne sont potentiellement plus à la charge de leurs parents.

Résultats des régressions logistiques et mise en œuvre dans le modèle démographique
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Les résultats du modèle logistique de mise en couple sont présentés dans le tableau suivant :

.. csv-table:: Logit - Coefficients des transitions de mise en couple
   :widths: 20 20
   :header-rows: 1
   :align: center
   :file: csv_files/trans_unions.csv

Les résultats du modèle logistique de séparation sont présentés dans le tableau suivant :

.. csv-table:: Logit - Coefficients des transitions de séparations
   :widths: 20 20
   :header-rows: 1
   :align: center
   :file: csv_files/trans_divorces.csv

La mise en œuvre des transitions de mise en couple et de séparation dans le modèle démographique est réalisée par un tirage uniforme, indépendant par individu dominant, et une mise en couple ou une séparation survient lorsque le résultat de ce tirage est inférieur à la probabilité logistique prédite.

Pour l'individu dominant *D1* nouvellement en couple, les caractéristiques du nouveau conjoint *C1* sont attribuées en tirant d'abord aléatoirement un autre individu dominant *D2* ayant le même genre et le même niveau de scolarité que *D1*. Les caractéristiques du conjoint *C2* (âge, genre et scolarité) sont alors attribuées au nouveau conjoint *C1* du dominant *D1* nouvellement en couple. Dans un premier temps, on restreint le bassin de tirage aux dominants *D2* qui ont un écart d'âge avec leur conjoint *C2* qui est inférieur à 5 ans (en valeur absolue). Si, pour un dominant *D1*, aucun conjoint n'est identifié en appliquant cette restriction d'écart d'âge, alors on réalise un second tirage dans le bassin des dominants *D2* qui ont le même genre et le même niveau de scolarité que *D1*, et qui ont un écart d'âge avec leur conjoint *C2* inférieur à 20 ans (en valeur absolue).

Il faut également préciser que dans la version actuelle de SimGen, le nouveau conjoint *C1* qui est attribué au dominant *D1* est systématiquement du sexe opposé. De futures versions du modèle pourront intégrer une représentation plus diversifiée des unions matrimoniales.

Décès
-----

Chaque année *t*, un individu d'âge *a* et de genre *g* a une probabilité *P(t,a,g)* de décéder. Cette probabilité, définie comme un taux de mortalité, est calculée à partir des quotients prospectifs de mortalité selon l'âge et le sexe estimés par Statistique Canada entre 2013-2014 et 2062-2063 (juillet-juin) pour les provinces et territoires. Le `rapport technique  <https://www150.statcan.gc.ca/n1/pub/91-620-x/91-620-x2014001-fra.pdf>`_ de Statistique Canada présente la méthodologie et les hypothèses de ces quotients prospectifs.

L'âge, le genre et la cohorte de naissance sont donc les seuls déterminants de l'espérance de vie des individus. Notons également que les immigrants et les natifs ont des probabilités équivalentes de décès en fonction de leur âge, de leur genre et de leur cohorte.

Migrations
----------

Le taux prospectif d'immigration internationale est égal à 6,6‰. Ce taux est calculé en divisant `le nombre d'immigrants projeté dans le scénario de référence de l'ISQ (55 000) <https://bdso.gouv.qc.ca/docs-ken/multimedia/PB01661FR_Perspective_demo2019H00F00.pdf>`_ par la `population québecoise enregistrée par Statistique Canada en 2017 (8 302 063) <https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000501&pickMembers%5B0%5D=1.6&pickMembers%5B1%5D=2.1&cubeTimeFrame.startYear=2016&cubeTimeFrame.endYear=2020&referencePeriods=20160101%2C20200101>`_. Les caractéristiques socio-économiques et démographiques des nouveaux immigrants internationaux sont attribuées en fonction des immigrants internationaux récents issus de la BDSPS de Statistique Canada pour l'année 2017. Chaque année *t*, on tire aléatoirement 0,0066*Population(t) nouveaux immigrants parmi ceux de l'année 2017. Les caractéristiques socio-économiques et démographiques des nouveaux immigrants sont alors celles des immigrants tirés de la BDSPS de 2017: l'âge, le genre, le niveau de scolarité, la présence de conjoint et le nombre d'enfants.

Les caractéristiques des émigrants dépendent uniquement de l'âge. L'émigration intègre les émigrants internationaux ainsi que le solde migratoire interprovincial. À chaque âge donné, la probabilité d'émigrer est égale pour toutes les personnes dominantes. Les émigrants d'un âge donné sont tirés de manière aléatoire. De plus, on considère que le(la) conjoint(e) du dominant ainsi que tous ses enfants âgés de moins de 18 ans émigrent avec la personne dominante. Le taux d'émigration par âge est calculé à partir du nombre d'émigrants interprovinciaux par classe d'âge en 2018-2019 du `tableau 17-10-0015-01 "Estimations des composantes de la migration interprovinciale, par âge et sexe, annuelles"  <https://www150.statcan.gc.ca/t1/tbl1/fr/tv.action?pid=1710001501>`_, du nombre d'émigrants internationaux par classe d'âge en 2018-2019 du `tableau 17-10-0014-01 "Estimations des composantes de la migration internationale, par âge et sexe, annuelles"  <https://www150.statcan.gc.ca/t1/tbl1/fr/tv.action?pid=1710001401>`_ et de la population québécoise par classe d'âge au 1er juillet 2018 du `tableau 17-10-0005-01 "Estimations de la population au 1er juillet, par âge et sexe"  <https://www150.statcan.gc.ca/t1/tbl1/fr/tv.action?pid=1710000501>`_. À noter que le nombre d'émigrants interprovinciaux à chaque âge a été normalisé sur les hypothèses du `solde interprovincial annuel de l'ISQ (9 000 personnes) <https://bdso.gouv.qc.ca/docs-ken/multimedia/PB01661FR_Perspective_demo2019H00F00.pdf>`_. Les taux d'émigration par classe d'âge sont les suivants:

.. csv-table::
 :header: "Classe d'âge", "Taux d'émigration (‰)"
 :widths: 100, 100
 :align: center

 "15 à 19 ans", "1,37"
 "20 à 24 ans", "3,08"
 "25 à 29 ans", "5,03"
 "30 à 34 ans", "4,90"
 "35 à 39 ans", "3,74"
 "40 à 44 ans", "2,72"
 "45 à 49 ans", "2,00"
 "50 à 54 ans", "1,38"
 "55 à 59 ans", "0,99"
 "60 à 64 ans", "0,84"
 "65 à 69 ans", "0,82"
 "70 à 74 ans", "0,64"
 "75 à 79 ans", "0,65"
 "80 à 84 ans", "0,62"
 "85 à 89 ans", "0,55"
 "90 ans et plus", "0,41"
