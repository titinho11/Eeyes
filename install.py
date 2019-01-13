# Ce fichier abrite le code du ZCasino, un jeu de roulette adapté

import os

#1 - On installe les prerequis
print ("---------------------------------------------------")
print ("INSTALLATION DES PREREQUIS")
os.system("sudo sh prereq.sh")
print ("Prerequis installe !")
print ("---------------------------------------------------")

#2 - On install nodejs
print ("---------------------------------------------------")
print ("INSTALLATION DE NODEJS V8.4")
os.system("sh installNode.sh")
print ("NodeJS et NPM installe !")
print ("---------------------------------------------------")


#3 - On install les outils hyperledger composer
print ("---------------------------------------------------")
print ("INSTALLATION DES OUTILS HYPERLEDGER COMPOSER")
os.system("sh installComposer.sh")
print ("Les outils Hyperledger composer sont bien installe !")
print ("---------------------------------------------------")


#4 - On install Hyperledger Fabric
print ("---------------------------------------------------")
print ("INSTALLATION DE HYPERLEDGER FABRIC")
os.system("sudo sh installNetwork.sh")
print ("---------------------------------------------------")


#4 - On install le code metier sur Hyperledger Fabric
print ("---------------------------------------------------")
print ("INSTALLATION DU CHAINCODE Eeyes")
os.system("sh installNetworkTools.sh")
print ("---------------------------------------------------")

#4 - On lance l'utilitaire de test du projet
print ("---------------------------------------------------")
print ("UTILITAIRE DE TEST DE Eeyes")
os.system("python3 main.py")
print ("---------------------------------------------------")

