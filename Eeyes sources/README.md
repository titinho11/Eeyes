# Eeyes
Outils de compilation de procès verbaux electoraux et de sécurisation des résultats via une Blockchain

# Eeyes Network

Cette application permet aux utilisateur via l'application front end d'uploader des pvs ce qui appelera la transaction uploadPV, puis à restituer l'ensemble des résultats en recuperant l'ensemble des RecapPVs.

TEST:
- Exécuter la transaction initBC avec les données de SE-Config
- Créer, uploader des PVs en exécutant la transaction computePV

TODO:
- Vue permettant la configuration de la Session Electorale
- Appel depuis la vue de la transaction initSE
- Vue des resultats et appels à la récupération des assets (PVs, RecapPV)
- Voir comment enregistrer une image (PV) dans la BC
- Vue uploader PV
- OCR sur pv image pour en extraire les informations
- Exécution de la transaction computePV depuis les données extraites de l'OCR, depuis la vue
- Uploader les pvs en cascade depuis le code python, vers la transaction computePV
- Déploiement dans une image docker (NB: le produit final sera une image docker)
- Documentation

NB: les différentes vues qu'il y'aura sur la plateforme
- Vue creation et configuration SE
- Vue upload PV
- Vues consultation des resultats :
  - Vue consultation resultats globaux
  - Vue consultation resultats par section
  - Vue consultation resultats par candidat (les résultats d'un candidats dans les différentes sections
  - Vue consultation résultats par scrutateurs (les résultats donnés par les scrutateurs du candidat x, ORGANISM et AUTHENTIC sont considérés comme un candidat...)
- Des boutons sur l'interface permettant de :
  - Télécharger le fichier de configuration de la SE
  - Télécharger les fichiers json des resultats (les recapPV)
  
  ENVIRONEMENT DE DEPLOIEMENT

  - Au démarrage de la machine virtuelle, l'application python 
  de gestion du projet se lance et propose en prompt :

    -   Maintenant elle allume le réseau hyperledger et démarre le "container" de l'appli web. L'application installe le chaincode et démarre l'API.
    -   Créer ou éditer la SE-Config.json :
        - en fait, l'on dit qu'un seconfig existe déjà, et on propose de l'éditer (via mousepad) ou de génerer un autre plus complexe( touche 2)
        - Si l'on appuie la touche 1 pour éditer, on ouvre mousepad, avec le fichier par défaut de seconfig. Dès lors que l'on ferme le mousepad, l'application demande de confirmer si l'on veut utiliser la seconfig éditée, et l'on teste sa structure via un script. Si tout est bon on avance à l'étape suivante. Si c'est refusé, l'application ramène au choix de modifier ou créer le fichier seconfig
        - Si l'on appuie sur la touche 2 pour générer un fichier seconfig, l'utilitaire est lancé en demandant les paramètres. A  la fin l'application ouvre le fichier généré, ensuite demande une confirmation.
    -   Actuellement le script demande d'aller à l'url 192.168.1.2/eeyes.html pour créer la session électorale avec le fichier seconfig qui se trouve dans le repertoire specifié, et demande de valider lorsque c'est fait.
    -   Ensuite l'on propose à l'utilisateur de générer les pvs, en lancant l'utilitaire de génération des pvs, il entre les paramètres et le chemin de sortie ( le dossier de sortie des json, et dans une section, creer un dossier caché ou l'on va mettre les fichies json), et ca génère dans le dossier en question.
    -   Le script demande d'aller sur la plate forme uploader un pv et de taper 1 dès que c'est fait. Ensuite, il demande de supprimer le pv ou les pvs précédemment uploadés du repertoire pour éviter de les renvoyer encore au système. L'on peut consulter déjà les resultats après chaque upload.
    -  Le script propose d'uploader rapidement tous les pvs, en exécutant le script d'upload. En cas de refus la procédure continue, sinon le script d'upload est ouvert.
    -  Le script dit que c'est terminé, et qu'on ne pourra plus uploader lorsque la date de la fin de la session va arriver.
    -  Le script demande si l'on veut recommencer l'essai depuis le début ou arrêter le systeme (1 ou 2). si 1 revenir sur la partie de création de seconfig. Exécuter le script d'extinction propre sur les dockers, puis la machine.

    SCRIPTS
    -   Créer seconfig
    -   Eteindre docker et éteindre vm
    -   Upload pvs
    -   Génération pvs
    -   Programme d'accueil

    #1 - On demarre les "container" docker
dans le dossier du code
composer archive create -t dir -n .

cd ~/fabric-dev-servers
export FABRIC_VERSION=hlfv11
./stopFabric.sh
./teardownFabric.sh
./startFabric.sh

composer card create -p connection.json -u PeerAdmin -c Admin@example.com-cert.pem -k c6211e0b87d5ac94276dbf92e4cfadf385ee78e1c46cffb9a2e454e090736065_sk -r PeerAdmin -r ChannelAdmin

composer card import -f PeerAdmin@eeyes-network.card 


#2 - On installe le chaincode
composer network install -c PeerAdmin@eeyes-network -a eeyes-network@0.0.1.bna
composer network start --networkName eeyes-network --networkVersion 0.0.1 -A admin -S adminpw -c PeerAdmin@eeyes-network
composer network ping -c admin@eeyes-network

composer card import -f admin@eeyes-network.card
 ?
