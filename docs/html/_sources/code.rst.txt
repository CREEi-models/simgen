Documentation des fonctions de SimGen
=====================================

.. automodule:: simgen

Données
-------

Les fonctions de données permettent de préparer les données pour la simulation. 

.. currentmodule:: simgen 

.. autofunction:: bdsps

.. autofunction:: isq

.. autoclass:: parse
    :members: dominants, spouses, kids

.. autoclass:: population
    :members: input

Transitions
-----------
.. autoclass:: update
    :members: params_birth, birth

Simulation
----------

La classe permetant de faire les simulations est model. Voici sa descriptions.

.. autoclass:: model
    :members: startpop, immig_assumptions, birth_assumptions, dead_assumptions, set_statistics, reset, next, simulate

Statistiques
------------

La classe permet de faire des statistiques dans le cadre d'une simulation. 

.. autoclass:: statistics
    :members: start, add, freq, prop

