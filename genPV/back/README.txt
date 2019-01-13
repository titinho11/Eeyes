Pour lancer la génération de pv, il faut taper une commande respectant le format suivant

python Gen_Pv_Files.py <Type de génération> <Type de coalition> <Probabilité de présence de scrutateur> <Location files>

*   le champ 'Type de génération' peut prendre les valeurs 'normal', 'chaos', 'fraude' ou 'coalition'

*   le champ 'Type de coalition' n'existe que si le précédent champ a pour valeur 'coalition' et dans ce cas pourra
        prendre l'une des valeurs suivantes 'equilibre' ou 'concentre'

*   le champ 'Probabilité de présence de scrutateur' correspond à la probabilité qu'un candidat possède un scrutateur
    dans un bureau de vote
        il s'agit d'un nombre entre 0 et 1

*   le champ 'Location files' correspond au dossier sur le disque dur ou les fichiers des pvs seront stockés


NB: il est à préciser qu'il faut utiliser python3