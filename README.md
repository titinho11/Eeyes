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
  
  
