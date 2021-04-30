.. _resultats:

***********************
Résultats
***********************

Cette section présente brièvement les résultats du modèle SimGen et les compare aux données officielles du Québec.

Données de comparaison
############################################

Ces données proviennent de différentes sources officielles:

- Données pour la population totale de 1998 à 2018 (Figure 1): les données proviennent de séries de l'ISQ.
- Données de projections de population (Figures 1 & 2): les projections de population sont basées sur le scénario moyen de l'ISQ à partir des données corrigées du recensement de 2016. Pour plus d'information concernant la méthodologie utilisée pour le calcul des projections de population, se référer au rapport "`Perspectives démographiques du Québec et des régions, 2016-2066, édition 2019 <https://statistique.quebec.ca/fr/fichier/perspectives-demographiques-du-quebec-et-des-regions-2016-2066-edition-2019.pdf>`_" produit par l'ISQ.
- Données par niveau de scolarité (Figure 3): les données concernant le plus haut niveau de scolarité atteint proviennent des fichiers de microdonnées à grande diffusion des recensements de 2006, 2011 et 2016. Ces données sont disponibles par l'entremise de l'Initiative de démocratisation des données (IDD_) de Statistique Canada.
- Données pour personnes en couple (Figure 4): ces données proviennent des estimations de la population au 1er juillet, selon l'état matrimonial ou l'état matrimonial légal, l'âge et le sexe (Tableau: 17-10-0060-01), qui sont produites par `Statistique Canada`_.

.. _IDD: https://www.statcan.gc.ca/fra/idd/idd-collection
.. _Statistique Canada: https://www150.statcan.gc.ca/t1/tbl1/fr/cv.action?pid=1710006001

Données de simulation
#####################

Comme mentionné précédemment, la base de données de départ de SimGen est tirée de la `Base de données de simulation de politiques sociales (BDSPS) <https://www.statcan.gc.ca/fra/microsimulation/bdmsps/bdmsps>`_.

Pour ce qui est des résultats analysés, ceux-ci proviennent d'une simulation de 2017 à 2040 utilisant les hypothèses suivantes: ::

    reference = model(start_yr=2017,stop_yr=2040)
    reference.startpop('startpop')
    reference.immig_assumptions(init='newimmpop', num=0.0066)
    reference.birth_assumptions(scenario='reference')
    reference.dead_assumptions(scenario='low')

Résultats des comparaisons
##########################

Il est important de noter que l'objectif de cet exercice n'est pas de reproduire exactement
les projections des différentes agences statistiques,
mais d'illustrer les différences afin de mieux comprendre les éventuels impacts
sur les différents modules et les modèles utilisant les résultats de SimGen comme intrant.

Population totale
*******************

.. figure:: figure/pop_total.png

Les données de l'année d'initialisation du modèle SimGen en 2017 sont calibrées sur les données de population par âge et par genre de l'ISQ pour cette même année. La Figure 1 compare les projections de population totale du modèle SimGen (2017-2040) avec les projections réalisées par l'Institut de la statistique du Québec (ISQ) à partir de l'année 2017.

Le modèle SimGen reproduit avec fidélité les projections réalisées par l'ISQ. En 2040, la population totale obtenue par SimGen (9,29 millions d'habitants) est similaire à la population totale obtenue par l'ISQ (9,32 millions d'habitants).

Population par groupes d'âge
*****************************

.. figure:: figure/pop_age.jpg

La Figure 2 compare les projections de population par groupes d'âge réalisées avec SimGen avec les projections de l'ISQ pour les années 2017 à 2040.
On remarque que les deux séries de projections sont relativement similaires.

Les projections de la population âgée de 65 ans et plus sont quasiment identiques entre l'ISQ et SimGen.
Cette population devrait égaler 2,45 millions en 2040 selon l'ISQ et elle devrait égaler 2,43 millions la même année selon Simgen.
En revanche, les projections de population pour les 0-24 ans  et pour les 25-64 ans présentent de légères différences entre l'ISQ et SimGen.
En 2040, la population âgées de 0 à 24 ans devrait égaler 2,37 millions selon l'ISQ et elle devrait égaler 2,08 millions selon Simgen.
La même année, la population âgées de 25 à 64 ans devrait égaler 4,51 millions selon l'ISQ et elle devrait égaler 4,78 millions selon Simgen.

Niveau de scolarité
*******************

.. figure:: figure/educ_2564.png

Premièrement, on remarque à la Figure 3 un saut entre les données du recensement de 2016 et celles projetées par SimGen pour 2017 en ce qui concerne les proportions de population selon le plus haut niveau de scolarité atteint. Cet écart s'explique par le fait que la variable de scolarité n'est pas catégorisée de la même manière dans la base de données initiale et dans les données publiques des recensements. Il faudra donc porter une attention particulière à cette variable pour tous projets ayant pour objectif d'étudier le système québécois d'éducation.

Pour ce qui est des tendances générales, on remarque une augmentation de la proportion de personnes ayant obtenu un diplôme de niveau universitaire et une diminution de la proportion des trois autres niveaux de scolarité.

Personnes en couple
*******************

.. figure:: figure/union_15over.png

Concernant la part de personnes en couple, la Figure 4 met en évidence un léger décalage entre les données historiques de Statistique Canada et les projections de SimGen à la fin des années 2010. Cet écart est comparable à ceux observés `entre les estimations de population annuelles et le recensement <https://www12.statcan.gc.ca/census-recensement/2016/ref/guides/002/98-500-x2016002-fra.cfm>`_.

Les résultats de SimGen mettent en avant une légère diminution de la proportion de personnes de 15 ans et plus en couple au Québec pour l'ensemble de la période de projection.
