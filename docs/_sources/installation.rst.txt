.. _installation:


==============
Installation
==============

.. _installing-docdir:

SimGen est programmé en langage Python. Il est ainsi nécessaire de posséder la version 3.7 de Python ou une version supérieure pour faire fonctionner SimGen sur votre ordinateur. 
Malgré tout, si vous n'avez pas accès au logiciel Python mais que vous disposez d'un compte Google, il vous sera possible d'utiliser SimGen en accès à distance via *Google Colab*. 
Ainsi, il est possible d'avoir accès à SimGen selon trois méthodes présentées ci-dessous. 
Dans tous les cas, veillez lire les `conditions d'utilisation <https://pypi.org/policy/terms-of-use/>`_ du site internet *pypi* qui héberge le package.


.. admonition:: Important

  SimGen utilise par défaut la Base de données de simulation de politiques sociales (BDSPS) comme base de données de départ. Cette base de données nécessite toutefois une licence d'utilisation gratuite octroyée sur demande par Statistique Canada.

  La BDSPS est disponible par l'entremise de `l'Initiative de démocratisation des données (IDD) <https://www.statcan.gc.ca/fra/microdonnees/idd>`_ . 
  Les professeurs et étudiants `des établissements postsecondaires participants <https://www.statcan.gc.ca/fra/microdonnees/centres-donnees/communaute>`_ 
  possèdent ainsi une licence d'utilisation de la BDSPS par l'entremise de leur établissement.

  Si **vous possédez une licence**, écrivez à yann.decarie@hec.ca en fournissant une preuve de licence ou d'appartenance à un établissement postsecondaire participant à l'IDD.
  Un fichier .csv prêt à l'emploi dans SimGen vous sera ensuite envoyé.

  Si **vous ne possédez pas de licence**, vous devez faire une demande de licence pour la BDSPS en écrivant à statcan.spsdm-bdmsps.statcan@canada.ca (voir également le `site internet <https://www.statcan.gc.ca/fra/microsimulation/bdmsps/bdmsps>`_ de la BDSPS). Lorsque vous aurez obtenu cette licence, il vous suffira d'écrire à yann.decarie@hec.ca et un fichier .csv prêt à l'emploi dans SimGen vous sera envoyé.

Installation automatisée
**************************

Si Python est installé sur votre ordinateur et que vous avez accès à votre invite de commande, 
il est possible d'installer SimGen de manière automatisée en écrivant simplement cette commande dans l'invite de commande (terminal ou anaconda prompt): ::

  pip install simgen-creei

Par la suite, il est possible d'invoquer SimGen dans un notebook ou un script en tant que module de la manière suivante: ::

 import simgen

Installation manuelle
**************************

Si Python est installé sur votre ordinateur, mais que vous ne pouvez utiliser l'invite de commande,
il est possible d'installer manuellement SimGen en complétant les étapes suivantes:

#. Allez sur le site internet `Pypi <https://pypi.org/>`_ et faites une recherche du package "simgen-creei".
#. Cliquez sur l'onglet "simgen-creei x.x.x", où "x.x.x" correspond au numéro de version.
#. Ensuite, cliquez sur "Download files" dans le menu à gauche et puis cliquez sur le nom du fichier "simgen-creei x.x.x.tar.gz" pour télécharger le fichier compressé.
#. Une fois le fichier téléchargé, décompressez le fichier "simgen-creei x.x.x.tar.gz" une première fois.
#. Ouvrez le dossier créé par l'extraction (ex. simgen-creei x.x.x.tar), continuez ensuite en ouvrant le dossier "dist" et décompressez le fichier "simgen-creei x.x.x.tar".
#. Une fois le fichier décompressé, transférez le dossier "simgen-creei x.x.x" qui en résulte dans le dossier où vous entreposez vos packages (si vous n'en avez pas, créez-en un à l'endroit qui vous convient le mieux).
#. Enfin, ajoutez dans votre notebook ou votre script le chemin d'accès de votre dossier de packages et vous pourrez invoquer SimGen en tant que module de la manière suivante:

::

  import sys
  sys.path.append('.../packages')

  import simgen

Accès à distance
**************************

Si vous ne possédez pas ou ne pouvez pas avoir accès au logiciel Python,
il est possible d'utiliser SimGen par l'entremise de Google Colab.
Après avoir accédé à votre compte Google Colab ou en avoir créé un, vous n'avez
qu'à utiliser la commande suivante dans un notebook ou un script pour installer SimGen: ::

  pip install simgen-creei

Par la suite, il est possible d'invoquer SimGen en tant que module de la manière suivante: ::

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
