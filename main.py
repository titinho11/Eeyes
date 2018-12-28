# Ce fichier abrite le code du ZCasino, un jeu de roulette adapté

import os

#1 - On demarre les contenaires docker
print ("Starting Fabric Network and installing chaincode...")
os.system("sh startNetwork.sh")
print ("Eeyes Network up !")

#Intialisation de la boucle
rep = "yes"
while rep == "yes":
    os.system("composer network reset -c admin@eeyes")
    #3 - On gere la creation ou l'edition de SE-Config.json
    print ("Vous devez actuellement creer un fichier de configuration" +
    " la session electorale. Il contient les informations relative" +
    " a la session electorale liee au au systeme de compilation" +
    " des proces verbaux Eeyes.")
    
    res = "no"
    while res == "no":
        print("Entrez le pays ou se deroule le scrutin...")
        pays = input()
        print("Entrez un titre pour cette session electorale...")
        title = input()
        print("Entrez la date de debut du scrutin...")
        debut = input()
        print("Entrez la date de fin du scrutin...")
        fin = input()
        print("Entrez la date limite de telechargement des proces verbaux...")
        dateFin = input()
        print("Entrez le nom de l'organisme en chargede l'organisation du scrutin...")
        organism = input()
        print("Entrez la profondeur des divisions (sections sous sections, sous sous sections etc...) a generer...")
        prof = input()
        print("Entrez le nombre de sections enfant par section a generer...")
        ss = input()
        print("Entrez le nombre d'electeurs inscrits par bureau de vote...")
        nbreInscrit = input()
        print("Entrez tour a tour les differents candidats a ce scrutin, saisissez par 'exit' pour terminer l'entree des candidats...")
        j = 0
        data = ""
        candidates = []
        while data != "exit":
            j+=1
            if j==1 :
                print("nom du candidat numero ",j,"...(s'il existe un candidat sortant, commencez obligatoirement par lui)")
            else :
                print("nom du candidat numero ",j,"...")
            data = input()
            if data != "exit":
                candidates.append(data)
        #enregistrement des candidats dans un fichier temporaire
        fichier = open("candidates.temp", "w")
        for item in candidates:
            fichier.write(item + "\n")
        fichier.close()

        print("Generation du fichier de configuration de la session electorale...")
        command = "python3 Gen_SE_Config.py " +prof+ " " +ss+ " . \"" +pays+ "\" \"" +title+ "\" \"" +debut+ "\" \"" +fin+ "\" \"" +dateFin+"\" \"" +organism+ "\" " +nbreInscrit+ " candidates.temp"
        print("voici la commande : "+command)

        os.system(command)
        os.remove("candidates.temp")
        print("Le fichier de configuration a bien ete genere !")
        print("Veuillez le consulter puis fermer l'editeur, sans neccessairement modifier quoique ce soit, puis revenez ici confimer son utilisation pour la suite...")
        os.system("se.json")
        print("Voulez-vous utiliser ce fichier de configuration ? entrez 'yes' pour confirmer et 'no' pour pour recommencer la generation...")
        res = input()

    #proposer de use le par defaut

    #4 - On cree la SE
    print("Creation de la session electorale dans le systeme Eeyes a partir du fichier de configuration...")
    os.system("python3 sendSEConfig.py")
    print("La session electorale est a present correctement configuree. Vous pouvez des a present consulter la plateforme web a travers le fichier html eeyes.html sur le bureau.")

    #reset BC : composer network reset -c admin@eeyes

    #5 - Generation des pvs
    print("GENERATION DES PROCES VERBAUX")
    print("Afin de generer les differents proces verbaux, veuillez fournir ces quelques informations")
    #print("GENERATION DES PROCES VERBAUX")
    command = "python3 genPVs.py "
    os.system(command)
    print("Les pvs sont generes. Vous pouvez donc acceder a la plateforme et les uploader un a un. Les resultats se mettent a jour apres chaque upload. Allez-y et uploadez quelques proces verbaux !")



    #6 - Upload des pvs
    print("---------------------------------------------------")
    print("Vous pouvez cependant utiliser un utilitaire pour uploader automatiquement tous les pvs, afin de vous eviter d'avoir a uploader plus de 50 fichiers !")
    print("Uploader automatiquement les pvs ? (si vous l'avez deja fait manuellement, entrez 'no') entrez 'yes' pour uploader automatiquement et 'no' si vous ne le voulez pas.")
    res = input()
    if res == "yes":
        os.system("python3 sendPvs.py")

    print("Accedez a la plateforme et consultez les resultats !!")
    print("------------------------------------------------------")
    print("processus de test termine. Vous pouvez le recommencer, avec un nouveau fichier de configuration de session electorale.")
    print("Recommencer le test ? entrez 'yes' pour recommencer a partir de la generation du fichier de configuration, et 'no' pour fermer le systeme et eteindre la machine.")
    rep = input()

#7 - On eteind le reseau Eeyes
print ("Test done ! Now we are going to shutdown the Eeyes Network.")
os.system("sh stopNetwork.sh")
print ("eteindre la machine ? 'yes' pour eteindre 'no' sinon")
p = input()
if p == "yes":
    os.system("sudo shutdown now")