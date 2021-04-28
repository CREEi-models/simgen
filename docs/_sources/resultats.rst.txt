.. _resultats:

*********
Résultats
*********

Cette section présente brièvement les résultats du modèle SimGen et le compare aux données officielles du Québec.

Données de comparaison
############################################

Ces données proviennent de différentes sources officielles.

Données historiques
*******************

Pour la population de 2018-2018, il s'agit d'estimations de population constituant une série historique de populations comparables ayant servi à la construction des projections de population basées sur le recensement de 2016.

Données de projections de population
************************************

Les projections de population sont basées sur le scénario moyen de l'ISQ à partir des données corrigées du recensement de 2016. Pour plus d'information concernant la méthodologie utilisée pour le calcul des projections de population, se référer au rapport \"Perspectives démographiques du Québec et des régions, 2016-2066, édition 2019\" produit par l\'ISQ_.

.. _ISQ: https://www.stat.gouv.qc.ca/statistiques/population-demographie/perspectives/perspectives-2016-2066.pdf

Données par niveau de scolarité
*******************************

Les données concernant le plus haut niveau de scolarité atteint proviennent des fichiers de microdonnées à grande diffusion des recensements de 2006, 2011 et 2016. Ces données sont disponibles par l'entremise de l'Initiative de démocratisation des données (IDD_) de Statistique Canada.

.. _IDD: https://www.statcan.gc.ca/fra/idd/idd-collection

Données pour personnes en couple
********************************

Ces données proviennent des estimations de la population au 1er juillet, selon l'état matrimonial ou l'état matrimonial légal, l'âge et le sexe (Tableau : 17-10-0060-01), qui sont produites par `Statistique Canada`_.

.. _Statistique Canada: https://www150.statcan.gc.ca/t1/tbl1/fr/cv.action?pid=1710006001

Base de données de départ
*************************

Pour cet exemple les données populationnelles de base pour ce modèle provienennt de la Base de données de simulation de politiques sociales (BDSPS).
Pour plus de détails, consulter la section :ref:`import`.

Données de simulation
#####################

Pour ce qui est des résultats obtenus à l'aide de SimGen, ils proviennent d'une simulation de 2017 à 2040 utilisant le scénario de référence. ::

    reference = model(start_yr=2017,stop_yr=2040)
    reference.startpop('startpop')
    reference.immig_assumptions(init='newimmpop')
    reference.birth_assumptions(scenario='reference')
    reference.dead_assumptions(scenario='medium')

Comparaison
###########

Il est important de noter que l'objectif de cet exercice n'est pas de reproduire exactement les projections des différentes agences statistiques, mais d'illustrer les différences afin de mieux comprendre les éventuels impacts sur les différents modules et modèles utilisant SimGen.

Population totale
*****************

.. figure:: figure/pop_total.jpg

Les données de l'année d'initialisation du modèle SimGen en 2017 sont calibrées sur les données de population par âge et par genre de l'ISQ pour cette même année. La Figure 1 compare les projections de population totale du modèle SimGen (2017-2040) avec les projections réalisées par l'Institut de la statistique du Québec (ISQ) à partir de l'année 2017.

Le modèle SimGen reproduit avec fidélité les projections réalisées par l'ISQ. En 2040, la population totale obtenue par SimGen (9,27 millions d'habitants) est similaire à la population totale obtenue par l'ISQ (9,32 millions d'habitants).

Population par groupe d'âge
***************************

.. figure:: figure/pop_age.jpg

La Figure 2 compare les projections de population par groupe d'âge réalisées avec SimGen avec les projections de l'ISQ pour les années 2017 à 2040.

On remarque que les deux séries de projection sont similaires. Par contre, les projections de population de SimGen pour les 0-24 ans et pour les 65 ans et plus sont relativement inférieures aux projections de l'ISQ. En 2040, la population âgée de 0 à 24 ans (respectivement 65 ans est plus) serait de 2,1 millions (respectivement 2,34 millions) selon SimGen, alors qu'elle serait égale à 2,37 millions (respectivement 2,45 millions) selon l'ISQ.

Niveau de scolarité
*******************

.. figure:: figure/educ_2564.png

Premièrement, on remarque à la Figure 3 un saut entre les données du recensement de 2016 et celles projetées par SimGen pour 2017 pour ce qui concerne les proportions de population selon le plus haut niveau de scolarité atteint. Cet écart s'explique par le fait que la variable de scolarité n'est pas catégorisée de la même façon dans la base de données initiale et dans les données de publiques des recensements. Il faudra donc porter une attention particulière à cette variable pour tous projets voulant étudier le système québécois d'éducation.

Pour ce qui est des tendances général, on remarque un augmentation de la proportion de personnes obtenant un diplôme de niveau universitaire et une baisse pour les trois autres niveaux.

Personnes en couple
*******************

.. figure:: figure/union_15over.png

Pour ce qui est de la part de personnes en couple, on remarque aussi à la Figure 4 que les niveaux ont un petit décalage par rapport aux estimations de Statistique Canada. L'écart observé ici est comparable à ce qui est observé dans certaines analyses plus poussées des familles au Canada_.

Pour ce qui concerne la tendance générale, on remarque que la proportion de personnes en couple reste stable chez les 15 ans et plus au Québec pour l'ensemble de la période de projection.

.. _Canada: https://www12.statcan.gc.ca/census-recensement/2016/ref/guides/002/98-500-x2016002-fra.cfm
