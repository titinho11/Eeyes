# Eeyes
Outils de compilation de procès verbaux electoraux et de sécurisation des résultats via une Blockchain

# Eeyes Network

Cette application permet aux utilisateur via l'application front end d'uploader des pvs ce qui appelera la transaction uploadPV, puis à restituer l'ensemble des resultats en recuperant l'ensemble des RecapPVs.

TEST:
- executer la transaction initBC avec les données de SE-Config
- Creer uploader des PVs en executant la transaction computePV

TODO:
- vue permettant la configuration de la SE
- appel depuis la vue de la transaction initSE
- vue des resultats et appels à la recuperation des assets (PVs, RecapPV)
- Voire comment enregistrer une image (PV) dans la BC
- Vue uploader PV
- OCR sur pv image pour en extraire les informations
- execution de la transaction computePV depuis les données extrait de l'OCR, depuis la vue
- uploader les pvs data en cascade depuis le code python, vers la transaction computePV
- Déploiement dans une image dockerr (NB: le produit final sera une image docker)
- Documentation

--------
TODO DEPLOIEMENT
----------
-   Integrer la creeation des pv
-   Integrer l'envoie des pvs
-   Integrer l'envoie de seconfig
-   Corriger et integrer les vues
-   Faire le doc de deploiement.

NB: les différentes vue qu'il y'aura sur la plateforme
- Vue creation et configuration SE
- Vue upload PV
- Vues consultation des resultats :
  - Vue consultation resultats globaux
  - Vue consultation resultats par section
  - Vue consultation resultats par candidat (les resultats d'un candidats dans les différentes sections
  - Vue consultation resultats par scrutateurs (les resultats donnés par les scrutateurs du candidat x, ORGANISM et AUTHENTIC sont considéré comme un candidat...)
- Des boutons sur l'interface permettant de :
  - Télécharger le fichier de configuration de la SE
  - Télécharger les fichiers json des resultats (les recapPV)
  
  ENVIRONEMENT DE DEPLOIEMENT

  - Au demarrage de la machine virtuelle, l'application python 
  de gestion du projet se lance et propose en prompt :

    -   Maintenant ca allume le reseau hyperledger et ca demarre le contenaire de l'appli web. ca installe le chaincode. ca demarre l'api.
    -   Creer ou editer la SE-Config.json :
        - en fait, on te dis que un seconfig existe deja, et on te propose de l'editer (via mousepad) ou de generer un autre plus complex( touche 2)
        - Si tu tape la touche 1 pour editer, on open mousepad, avec le fichier par defaut de seconfig. des lors que tu referme le mousepad la, on te demande de confirmer que tu veux utiliser la seconfig la, et on teste sa structure via un script. si tout est bon on avance a l'etape suivante. si tu refuse, on te ramene au choix de modifier ou creer le fichier seconfig
        - si tu tape la touche 2 pour generer un fichier seconfig, ca lance l'utilitaire en te demandant les params... a la fin ca t'ouvre le fichier generer, puis a la fin ca te redemande si tu confirme ca ou pas.
    -   Actu ca te demande d'aller a l'url 192.168.1.2/eeyes.html pour creer la se avec le fichier seconfig qui se trouve dans le repertoire specifie, et te demande de valider lorsque c'est fait
    -   Ensuite on lui propose de generer les pv, en lancant l'utilitaire de generation des pvs, il entre les params et le chemin de sortie (erase le dossier de sortie des json, et dans une section creer un dossier cache ou on va mettre les json), et ca genere labas.
    -   ca te demande d'aller sur la plate forme uploader un pv et de taper 1 des que c'est fait.ca te demande de supprimer le pv ou les pvs precedemment uploades du repertoire la pour eviter de les renvoyer encore au systeme. ca te demande de consulter deja les resultats apres chaque upload.
    -   ca te propose d'uploader rapidement tous les pvs la, en executant le script d'upload. si tu refuse ca avance, sinon, ca ouvre le script d'upload et a la fin ca avance.
    -   ca te dit que c'est termine, et qu'on ne pourra plus uploader lorsque la datte de la fin de la session va arriver.
    -   ca te demande si tu veux recommencer l'essaie depuis le debut ou eteindre le systeme (1 ou 2). si 1 boucle sur la partie de seconfig. executer script extintion propre les docker, puis la machine.

    SCRIPTS
    -   Creer seconfig
    -   eteindre docker et eteindre vm
    -   upload pvs
    -   generation pvs
    -   programme d'acceuil ci