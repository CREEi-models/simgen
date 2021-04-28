.. _utilisation:

*****************
Utilisation
*****************

Cette section a pour objectif de guider les utilisateurs de SimGen dans l'utilisation de celui-ci.
Dans un premier temps, les étapes d'utilisation et les différents choix possibiles de paramètres sont présentés.
Par la suite, un exemple de notebook/script est proposé afin de servir de point de départ
aux utilisateurs pour le lancement de simulations et l'analyse des résultats.

Étapes
===========
Lors de la rédaction d'un notebook ou d'un script Python, quatre étapes principales doivent être suivies afin d'obtenir des résultats de simulation avec SimGen :

1. Choix des paramètres d'utilisation
***************************************

La première étapes consiste à choisir les paramètres qui guideront SimGen par rapport à la localisation de la base de données de départ et
aux hypothèses de modélisation.

**Sentier d'accès et nom du fichier de la BDSPS**

Un premier paramètre d'utilisation à déterminer est le sentier d'accès et le nom du fichier .csv
qui vous aura été fourni par l'équipe du CREEi et qui correspond à une version épurée de
la `Base de données de simulation de politiques sociales (BDSPS) <https://www.statcan.gc.ca/fra/microsimulation/bdmsps/bdmsps>`_.
En début de notebook/script, il est suggéré de définir un objet qui comprend le sentier d'accès et le nom du fichier
de la BDSPS selon l'endroit où vous aurez enregistré le fichier, et le nom que vous lui aurez donné :  ::

 donnees_brutes = '.../bdsps2017_slice.csv'

Cet objet servira d'intrant dans la fonction de formattage des données (*bdsps_format()*) à l'étape d'initialisation du modèle.

**Année de fin**

L'année de fin de la simulation détermine la durée des projections effectuées par SimGen. Les valeurs possibles vont de 2018 à 2100.
Ce paramètre doit figurer comme intrant dans la fonction de création d'instance de classe de SimGen (*model()*), qui est couvert plus en détails à l'étape d'initialisation du modèle.

**Nombre de réplications**

Le nombre de réplications détermine le nombre de fois où SimGen simule l'ensemble de l'horizon de temps (année de début à l'année de fin) dans une simulation.
Ce paramètre est fixé par défaut à 1. Lorsque le nombre de réplication est supérieur à 1, les résultats de la simulation correspondent à la moyenne des résultats des réplications.

Il est suggéré d'utiliser plus d'une réplication afin d'obtenir des résultats uniformes d'une simulation à une autre.
Le nombre optimal de réplications varie selon les résultats utilisés. Les résultats précis comprenant un petit nombre d'observations (ex. : le nombre de personnes en couple de 95 ans) sont plus susceptibles de varier
d'une simulation à une autre qu'un résultat global comportant un grand nombre d’observations (ex. : le nombre total de personnes en couple âgées de 15 à 65 ans).
Les résultats précis nécessitent donc un plus grand nombre de réplications pour être stables (50 réplications),
que les résultats globaux (10 réplications).


**Hypothèses**

*Fécondité*

Dans SimGen, il est possible de calibrer le nombre de naissances selon trois scénarios de `fécondité <https://bdso.gouv.qc.ca/docs-ken/multimedia/PB01661FR_Perspective_demo2019H00F00.pdf>`_ issus du plus récent document de projection démographique de l'Institut de la statistique du Québec (ISQ).
Les scénarios supposent la convergence de l'indice synthétique de fécondité (ISF) vers les trois valeurs suivantes d'ici 2026 :

=============  ======
Scénario       ISF
=============  ======
Faible (weak)  1,45
Référence      1,60
Fort (strong)  1,75
=============  ======

Dans le version actuelle de SimGen, les termes anglais *weak*, *reference*, et *strong* doivent être utilisés comme intrant dans la fonction d'hypothèse de fécondité.
Il est suggéré de définir un objet qui comprend le nom du scénario de fécondité choisi comme suit : ::

 fecondite = 'reference'

Cet objet sere utilisé à l'étpae 2 lors du chargement des des principaux intrants.

*Mortalité*

Il est possible de fixer les quotients de mortalité selon trois scénarios de `mortalité  <https://www150.statcan.gc.ca/n1/pub/91-620-x/91-620-x2014001-fra.pdf>`_ issus du plus récent document de projection démographique de Statistique Canada.
Les scénarios supposent l'atteinte de trois valeurs possibles de l'espérance de vie à la naissance selon le genre d'ici 2062 :

==============  ========  ========
Scénario        Hommes    Femmes
==============  ========  ========
Faible (low)    89,8 ans  92,0 ans
Moyen (medium)  87,5 ans  89,2 ans
Élevé (high)    85,9 ans  87,3 ans
==============  ========  ========


En 2020, l'espérance de vie à la naissance est estimée à 80,6 ans pour les hommes et 84,0 ans pour les femmes (`ISQ, mars 2021 <https://statistique.quebec.ca/fr/communique/baisse-de-lesperance-de-vie-au-quebec-en-2020-a-la-suite-de-la-hausse-marquee-du-nombre-de-deces>`_).
Dans le version actuelle de SimGen, les termes anglais *weak*, *medium*, et *strong* doivent être utilisés comme intrant dans la fonction d'hypothèse de mortalité.
Il est suggéré de définir un objet qui comprend le nom du scénario de mortalité choisi comme suit : ::

 mortalite = 'low'

Cet objet sere utilisé à l'étpae 2 lors du chargement des des principaux intrants.

*Immigration*

Dans SimGen, le nombre de nouveaux immigrants par année est déterminé par le taux prospectif d'immigration internationnale
(proportion de nouveaux immigrants par rapport à la population totale).
Ce paramètre est fixé par défaut à une valeur de 0,0066.
Cette valeur correspond à 55 000 nouveaux immigrants internationnaux en 2017 (sur une population totale de 8 302 063),
conformément au scénario de référence du plus récent `document <https://bdso.gouv.qc.ca/docs-ken/multimedia/PB01661FR_Perspective_demo2019H00F00.pdf>`_ de projection démographique de l'ISQ.

Le paramètre de taux prospectif d'immigration internationnale peut être fixé à la valeur désirée (supérieure ou égale à 0).
Ce paramètre reste toutefois fixe durant toutes les années de la simulation.
Cette caractéristique implique une augmentation graduelle du nombre de nouveaux immigrants suivant la croissance de la population totale.

Si l'utilisateur souhaite modifier l'hypothèse d'immigration, il est suggéré de définir un objet qui comprend le taux d'immigration internationnale choisi comme suit : ::

 taux_immigration = 0.0066

Cet objet sere utilisé à l'étpae 2 lors du chargement des des principaux intrants.
Il est à noter que les caractéristiques des nouveaux immigrants sont issues des immigrants récents (depuis 5 ans ou moins) de la BDSPS de 2017.


2. Initialisation du modèle
*********************************

L'initialisation du modèle vise à charger en mémoire l'ensemble des informations nécessaires au lancement de la simulation.
Cette étape se divise en plusieurs sous-étapes.

**Importation des packages**

SimGen utilise certains packages standards, qu'il est nécessaire d'importer : ::

 import warnings
 import pandas as pd
 import numpy as np
 from matplotlib import pyplot as plt
 warnings.filterwarnings("ignore")

**Importation des fonctions et des classes de SIMGEN**

Il est ensuite nécessaire d'importer SimGen en tant que tel : ::

 import simgen
 from simgen import model, formating

**Formattage données de départ**

La fonction bdsps_format transforme la BDSPS de Statistique Canada afin de mettre en forme certaines variables et créer les registres des individus (dominants, conjoints et enfants).
Cette fonction calibre également les poids des répondants, par âge et sexe, afin de s’arrimer à la population québécoise de 2017, selon l’ISQ. ::

 preparation_data=formating()
 preparation_data.bdsps_format(donnees_brutes)

où *donnees_brutes* correspond au sentier d'accès et au nom du fichier .csv de la BDSPS (ex. : donnees_brutes = '.../bdsps2017_slice.csv').

.. toggle-header::
    :header: **Détails : bdsps_format()**

    .. currentmodule:: simgen

    .. autoclass:: bdsps

|

**Création de l'instance du modèle**

La commande suivante crée un gabarit permettant entre autres de stocker les résultats propres à la simulation selon les paramètres d'utilisation choisis : ::

 base = model(stop_yr=annee_fin)

où *annee_fin* correspond à l'année de fin de la simulation (ex. : annee_fin = 2050).

.. toggle-header::
    :header: **Détails : classe model()**

    .. autoclass:: model
        :members: simulate

|


Pour être en mesure de lancer une deuxième simulation avec des paramètres d'utilisation différents et de comparer les résultats des deux simulations,
vous n'avez qu'à réutiliser cette commande en donnant un nom différent au gabarit : ::

  base2 = model(stop_yr=annee_fin)

où *annee_fin* correspond à l'année de fin de la simulation (ex. : annee_fin = 2050).

**Chargement des principaux intrants**

Tout d'abord, le chargement de la base de données de départ s'effectue à l'aide de la commande suivant : ::

 base.startpop('start_pop')

où *start_pop* est le nom donné par défaut à la base de données de départ à la suite du formattage de la BDSPS.

.. toggle-header::
    :header: **Détails : fonction startpop()**

    .. autoclass:: model
        :members: startpop


|


Le chargement des hypothèses de la simulation s'effectue ensuite à l'aide des commandes suivantes et des objets définis à l'étape 1 (*taux_immigration*, *fecondite*, *mortalite*) : ::

 base.immig_assumptions(init='imm_pop', num=taux_immigration)
 base.birth_assumptions(scenario=fecondite)
 base.dead_assumptions(scenario=mortalite)

où *imm_pop* correspond à la la banque de données des immigrants récents produite par la fonction *bdsps_format()*.


.. toggle-header::
     :header: **Détails : fonction immig_assumptions()**

     .. autoclass:: model
        :members: immig_assumptions


|


3. Lancement de la simulation
*********************************

Le lancement de la simulation s'effectue à l'aide de la fonction suivante : ::

 base.simulate(rep=nb_rep)

où *nb_rep* correspond au nombre de réplications de la simulation (ex. : nb_rep = 100).

Il est à noter que cette commande a un temps d'exécution plus élevé que les commandes présentées précédemment.
Le temps de simulation croît de manière substantielle selon l'année de fin et le nombre de réplications.

.. toggle-header::
    :header: **Détails : fonction simulate()**

    .. autoclass:: model
        :members: simulate


|


4. Affichage des résultats
*********************************

Tout d'abord, le tableau ci-dessous présente la liste des variables pouvant servir lors de l'affichage des résultats de SimGen :

================  ========  ==========  ==========  ====================================
Variable          Nom       Type        Valeurs     Étiquette
================  ========  ==========  ==========  ====================================
Âge               age       Entier      0 à 110
Genre             male      Booléen     **True**    Homme

                                        **False**   Femme
Statut d'études   insch     Booléen     **True**    Aux études

                                        **False**   Études terminées
Niveau scolarité  educ      Caractères  *none*      Sans diplôme

                                        *des*       Secondaire

                                        *dec*       Collégial

                                        *uni*       Universitaire (Bacc. et supérieur)
Statut conjugal   married   Booléen     **True**    En union

                                        **False**   Célibataire
Nombre d'enfants  nkids     Entier      0 à 3+
================  ========  ==========  ==========  ====================================


**Production de résultats**

Il est possible de produire des résultats à l'aide de deux fonctions.
La fonction *stats.freq()* calcul le nombre d'individus selon le sous-groupe spécifié. Par exemple : ::

 population_hommes=base.stats.freq(sub='male==True')

Si aucun argument n'est inscrit dans la fonction, celle-ci calcule le nombre de personne dans l'ensemble de la population.

.. toggle-header::
    :header: **Détails : fonction stats.freq()**

    .. autoclass:: statistics
         :members: freq

|


La fonction *stats.prop()* calcule pour sa part la proportion de la population respectant les caractéristiques spécifiées. Par exemple :  ::

 proportion_niveau_scolarite = base.stats.prop('educ', sub="age>=25 and age<=64 and insch==False")

.. toggle-header::
    :header: **Détails : fonction stats.prop()**

    .. autoclass:: statistics
         :members: prop

|


**Sauvegarde des données**

Enfin, il est possible de sauvegarder les résultats de la simulation dans un fichier .pkl à l'aide de la commande suivante : ::

 base.stats.save('.../resultats_simgen')

.. toggle-header::
    :header: **Détails : fonction save()**

    .. autoclass:: statistics
         :members: save

|


Pour une descrption complète des classes et des fonctions de SimGen, consultez la page :ref:`code`.

Exemple
============

Simulation de base
*******************

Cet exemple de notebook permet de se familiariser avec l'utilisation de Simgen en effectuent une simulation
et en présentant des résutats de base.

**Téléchargement du notebook :**
 Cliquez :download:`ici <https://colab.research.google.com/drive/1Vrxo7kSp0_USMbECH-SlFdsZ3IYQwCCn?usp=sharing>`

**Accès au notebook via Google colab* :**
 Cliquez :download:`ici <https://colab.research.google.com/drive/1Vrxo7kSp0_USMbECH-SlFdsZ3IYQwCCn?usp=sharing>`

Il est à noter qu'il est nécessaire de posséder un compte Google pour utiliser Google colab.
