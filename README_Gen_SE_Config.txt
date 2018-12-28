Il faut savoir que pour nous une Session électorale est vue comme un arbre dont la racine est le pays ou ont lieu
les élections, chaque noeud est une section et les feuilles sont les bureaux de vote.

Pour lancer la génération de SE-config.json, il faut taper une commande respectant le format suivant

python Gen_SE_Config.py <Profondeur de l'arbre> <Nombre d'enfant> <Location file>

*   Le champ 'Profondeur de l'arbre' correspond à la prodondeur de l'arbre de la session électorale

*   Le champ 'Nombre d'enfant' correspond le nombre d'enfant par noeud

*   Le champ 'Location files' correspond au dossier sur le disque dur ou les fichiers des pvs seront stockés


NB:

-   Après création du fichier se.json, il faut le modifier pour y ajouter les iformations manquante sur la séssion
    électorale

-   Il est à préciser qu'il faut utiliser python3