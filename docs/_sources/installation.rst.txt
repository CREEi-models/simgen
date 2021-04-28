.. _premierpas:


*************
Installation
*************

.. _installing-docdir:


SimGen est programmé en langage Python. Il est donc nécessaire de posséder la version 3.7 de Python ou une version supérieure 
pour faire fonctionner SimGen sur votre ordinateur. 
Malgré tout, si vous n'avez pas accès au logiciel Python mais que vous disposez d'un compte Google, il vous 
sera possible d'utiliser SimGen en accès à distance via *Google colab* (Voir méthode 3). 

Ainsi, il est possible d'avoir accès à SimGen selon trois méthodes : 1) installation automatisée, 2) installation manuelle et 3) accès à distance. 
Celles-ci sont présentées ci-dessous. 
Pour rester informé.e des mises à jour de SimGen, inscrivez-vous à notre `liste d’envoi dédiée <http://eepurl.com/hs0YED>`_.
Il est à noter que SimGen est fourni "tel quel", sous une `licence MIT <https://rsi-models.github.io/CPR/credits.html#licence>`_.


.. admonition:: Important

  SimGen utilise par défaut la Base de données de simulation de politiques sociales (BDSPS) 
  comme base de données de départ. Cette base de donnée nécessite toutefois une licence d'utilisation gratuite octroyée sur demande par Statistique Canada. 
  
  La BDSPS est disponible par l'entremise de l'Initiative 
  de démocratisation des données (IDD). Les professeurs et étudiants des établissements 
  postsecondaires participants possèdent ainsi une licence d'utilisation de la BDSPS par l'entremise
  de leur établissement.

  Si **vous possédez cette licence**, 
  écrivez à yann.decarie@hec.ca et un fichier .csv prêt à l'emploi 
  dans SimGen vous sera envoyé.

  Si **vous ne possédez pas cette licence**, vous devez faire une demande de licence pour la BDSPS 
  en écrivant à statcan.spsdm-bdmsps.statcan@canada.ca (Voir également le `site internet <https://www.statcan.gc.ca/fra/microsimulation/bdmsps/bdmsps>`_ de la BDSPS). Lorsque vous aurez obtenu 
  cette licence, il vous suffira d'écrire à yann.decarie@hec.ca et 
  un fichier .csv prêt à l'emploi dans SimGen vous sera envoyé.  



Installation automatisée
==========================

Si vous avez accès à Python et à votre invité de commande, il est possible d'installer SimGen 
de manière automatisée en écrivant simplement cette commande dans l'invité de commande (terminal) : ::

  pip install simgen

Par la suite, il est possible d'importer SimGen dans un notebook ou un script en tant que module. ::

 import simgen 

Installation manuelle
===========================

Si vous avez accès au logiciel Python, mais que vous ne pouvez utiliser l'invité de commande, 
il est possible d'installer manuellement SimGen en suivant les étapes suivantes :

#. Allez sur le site internet `Pypi <https://pypi.org/>`_ et faites une recherche du package "simgen". 
#. Cliquez sur l'onglet "simgen-x.x.x", où "x.x.x" correspond au numéro de version.
#. Ensuite, cliquez sur "Download files" dans le menu à gauche et puis cliquez sur le nom du fichier "simgen-x.x.x.tar.gz" pour télécharger le fichier compressé.
#. Une fois le fichier téléchargé, décompressez le fichier "simgen-x.x.x.tar.gz" une première fois.
#. Ouvrez le dossier créé par l'extraction (ex. simgen-x.x.x.tar), continuez ensuite en ouvrant le dossier "dist" et décompressez le fichier "simgen-x.x.x.tar".
#. Une fois le fichier décompressé, transférez le dossier "simgen-x.x.x" dans le dossier où vous entreposez vos packages (Si vous n'en avez pas créez-en un à l'endroit qui vous convient le mieux).
#. Enfin, ajoutez dans votre notebook ou votre script le sentier d'accès de votre dossier de packages et vous pourrez importer SimGen en tant que module. 

::

  import sys
  sys.path.append('.../packages')

  import simgen


Accès à distance 
===================

Si vous ne possédez pas ou ne pouvez pas avoir accès au logiciel Python, 
il est possible d'utiliser SimGen par l'entremise de Google Colab. 
Après avoir accédé à votre compte Google Colab ou en avoir créé un, vous n'avez 
qu'à utiliser la commande suivante dans un notebook ou un script pour installer SimGen : ::

  pip install simgen

Par la suite, il est possible d'importer SimGen en tant que module : ::

 import simgen





..  Installation de SimGen
    ======================
    On peut installer facilement SimGen en suivant deux étapes. La première est de télécharger le simulateur depuis Github ::
    git clone https://github.com/creei-models/simgen simgen
    Ensuite on doit l'installer au terminal en allant a la racine du répertoire *simgen* ::
    python setup.py install
    Par la suite, on ne devrait pas travailler dans ce répertoire d'installation. Pour obtenir une nouvelle version, il suffit de répéter les étapes qui précèdent.
    Importer SimGen dans un notebook ou un script
    =============================================
    Pour importer SimGen dans un notebook ou un script Python, on ajoute:
    .. code:: ipython3
    import simgen
    On peut aussi importer des sous-modules spécifiques en utilisant:
    .. code:: ipython3
    from simgen import model, update, parse
    Rouler une première simulation
    ==============================
    On importe le modèle:
    .. code:: ipython3
    from simgen import model
    On déclare une instance avec année de départ et année d’arrêt.
    .. code:: ipython3
    base = model(start_yr=2017,stop_yr=2040)
    On donne le nom du fichier *pickle* qui contient la base de départ (un exemple se trouve dans simgen/params). Il peut être copié dans le répertoire de travail.
    .. code:: ipython3
    base.startpop('startpop')
    On donne les hypothèses d’immigration ainsi que le nom du fichier pour la population de nouveaux immigrants. Un exemple peut être copié dans le répertoire de travail et se trouve sous simgen/params.
    .. code:: ipython3
    base.immig_assumptions(init='newimmpop')
    On prend les hypothèses par défaut pour les naissances:
    .. code:: ipython3
    base.birth_assumptions()
    On prend aussi les hypothèses par défaut pour la mortalité:
    .. code:: ipython3
    base.dead_assumptions()
    On peut toujours réinitialiser à l'aide de *reset*.
    .. code:: ipython3
    base.reset()
    .. code:: ipython3
    base.pop.size()
    .. parsed-literal::
    8298827.000000236
    On peut faire une seule année en utilisant *next()*.
    .. code:: ipython3
    base.next()
    Pour faire rouler la simulation de l’année de départ à l’année de fin, on lance *simulate*:
    .. code:: ipython3
    time base.simulate()
    .. parsed-literal::
    2040
