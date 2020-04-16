.. _data:


*********************
Importer des données
*********************

.. _registers:

Compas permet d'utiliser des données de plusieurs sources. Cependant, une mise-en-forme particulière des données est nécessaire afin de les rendre utilisable par le simulateur.  

Les registres de données
========================

Compas utilise trois registres de données:
 
* registre dominant (hh)
* registre conjoint (sp)
* registre enfants (kd)

Le registre des dominants doit contenir une clé identifiante **nas** unique pour chaque dominant. Les conjoints des dominants sont listés dans le registre conjoint en utilisant cette même clé identifiante **nas**. Donc, un conjoint n'a pas son propre nas mais le **nas** du dominant qui est son conjoint. Dans un modèle ouvert, les conjoints, tout comme les enfants sont des acteurs fantômes. Le registre enfants doint être mis en forme de la même façon, en listant chaque enfants sur une ligne différente.  Donc, un dominant qui a un conjoint et 3 enfants aura une entrée dans le registre dominant et conjoint et trois entrées dans le registre enfants. 

Nous décrivons chacun des registres ici-bas: 


Mettre en forme des données sources
===================================

Dans Compas, une population est composé des trois registres ici-haut. La class

  
Population dans Compas
======================
