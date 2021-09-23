.. _code:

Dictionnaire (classes et fonctions)
========================================

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
    :members:  birth, marriage, divorce, dead, emig, educ

Simulation
----------
La classe permettant de réaliser les simulations est *model*. Voici sa description.

.. autoclass:: model
    :members: startpop, immig_assumptions, birth_assumptions, dead_assumptions, set_statistics, reset, next, simulate

La classe permettant de paralléliser le calcul des réplications est *replicate*. Voici sa description.

.. autoclass:: replicate
    :members: simulate

Statistiques
------------
La classe *replicate* permet également de produire des statistiques dans le cadre d'une simulation, lorsque cette classe est utilisée pour la simulation.

.. autoclass:: replicate
    :members: freq, prop, save

La classe *statistics* peut  être utilisée pour produire des statistiques, si la classe *model* est utilisée plutôt que *replicate* pour produire la simulation. Voici sa description. 

.. autoclass:: statistics
    :members: start, add, add_to_mean, freq, prop, save