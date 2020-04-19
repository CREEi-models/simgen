.. _premierpas:


***********************
Premier pas avec SimGen
***********************

.. _installing-docdir:

Installation de SimGen
======================

On peut installer facilement SimGen suivant deux étapes. La première est de télécharger de github ::

  git clone https://github.com/creei-models/simgen simgen 

Ensuite on doit l'installer au terminal en allant a la racine du repertoire simgen ::

  python setup.py install

Par la suite, nous ne devriez pas travailler dans ce répertoire d'installation. Pour aller chercher une nouvelle version, il suffit de répetez les étapes précédentes. 

Importer SimGen dans un notebook ou script
==========================================

Pour importer SimGen dans un notebook ou un script python on ajoute ::

  import simgen 

On peut aussi importer des sous-modules spécifiques en utilisant ::

  from simgen import model, update, parse
  
Rouler une première simulation
==============================

On importe le modèle:

.. code:: ipython3

    from simgen import model

On déclare une instance avec année de départ et d’arrêt.

.. code:: ipython3

    base = model(start_yr=2017,stop_yr=2040)

On donne le nom du fichier pickle qui contient la base de départ

.. code:: ipython3

    base.startpop('startpop')

On donne les hypothèses d’immigration ainsi que le nom du fichier pour
la population de nouveaux immigrants.

.. code:: ipython3

    base.immig_assumptions(init='newimmpop')

On prend les hypothèses par défaut pour les naissances

.. code:: ipython3

    base.birth_assumptions()

On prend aussi les hypothèses par défaut pour la mortalité

.. code:: ipython3

    base.dead_assumptions()

On peut toujours ré-initialiser avec reset.

.. code:: ipython3

    base.reset()

.. code:: ipython3

    base.pop.size()




.. parsed-literal::

    8298827.000000236



On peut faire juste une année en utilisant next()

.. code:: ipython3

    base.next()

Pour faire la simulation de l’année de départ à l’année de fin, on lance
simulate

.. code:: ipython3

    time base.simulate()


.. parsed-literal::

    2040
