# Ce fichier abrite le code du ZCasino, un jeu de roulette adapté

import os

#1 - On demarre les contenaires docker
print ("---------------------------------------------------")
print ("DEMARRAGE DE L'ENVIRONEMENT")
print ("Starting Fabric Network and installing chaincode...")
os.system("killall -9 node")
os.system("sudo sh startNetwork.sh")
os.system("sh installNetworkTools.sh")
print ("Eeyes Network up !")

#Intialisation de la boucle
rep = "yes"
while rep == "yes":
    os.system("composer network reset -c admin@eeyesv4")
    #3 - On gere la creation ou l'edition de SE-Config.json
    print ("---------------------------------------------------")
    print ("CREATION DU FICHIER DE CONFIGURATION DE LA SESSION ELECTORALE")
    print("\033[32m")
    print ("Vous devez actuellement creer un fichier de configuration" +
    " la session electorale. Il contient les informations relative" +
    " a la session electorale liee au au systeme de compilation" +
    " des proces verbaux Eeyes.")
    print("\033[37m")
    
    res = "no"
    while res == "no":
        os.system("rm ~/Desktop/SE-config.json 2>/dev/null")
        os.system("rm -r ~/Desktop/.Jsons 2>/dev/null")
        os.system("rm -r ~/Desktop/Images 2>/dev/null")
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
        command = "python3 Gen_SE_Config.py " +prof+ " " +ss+ " ~/Desktop \"" +pays+ "\" \"" +title+ "\" \"" +debut+ "\" \"" +fin+ "\" \"" +dateFin+"\" \"" +organism+ "\" " +nbreInscrit+ " candidates.temp"
        print("voici la commande : "+command)

        os.system(command)
        os.remove("candidates.temp")
        print("\033[32m")
        print("Le fichier de configuration a bien ete genere !")
#        print("Veuillez le consulter puis fermer l'editeur, sans neccessairement modifier quoique ce soit, puis revenez ici confimer son utilisation pour la suite...")
 #       os.system("gedit ~/Desktop/SE-config.json")
        print("Voulez-vous utiliser ce fichier de configuration ? entrez 'yes' pour confirmer et 'no' pour pour recommencer la generation...")
        print("\033[37m")
        res = input()

    #proposer de use le par defaut

    #4 - On cree la SE
    print ("---------------------------------------------------")
    print("\033[32m")
    print ("CREATION DE LA SESSION ELECTORALE")
    print("Creation de la session electorale dans le systeme Eeyes a partir du fichier de configuration...")
    print("\033[37m")
    os.system("python3 Send_SE_Config.py ~/Desktop")
    print("La session electorale est a present correctement configuree. Vous pouvez des a present consulter la plateforme web a travers le fichier html eeyes.html sur le bureau.")

    #reset BC : composer network reset -c admin@eeyes

    #5 - Generation des pvs

    print("\033[32m")
    print("-------------------------------------------")
    print("GENERATION DES PROCES VERBAUX")
    print("Afin de generer les differents proces verbaux, veuillez fournir ces quelques informations")
    print("Entrez le type de generation : ")
    print("Entrez 'normal' pour generer les proces verbaux identique pour chaque scrutateurs d'un meme bureau de vote")
    print("Entrez 'chaos' pour generer des proces verbaux differents (modifies) pour chaque scrutateurs d'un meme bureau de vote")
    print("Entrez 'fraude' pour generer des proces verbaux identique pour les scrutateurs du candidat sortant et ceux de l'organisme, le reste ayant des proces verbaux authentique")
    print("Entrez 'coalition' pour generer les proces verbaux identique pour tous les scrutateurs d'un meme groupe de candidat prit au hazard, et ce dans tous les bureau de vote")
    typegen = input()

    print("Entrez la probabilite de presence d'un scrutateur d'un candidat lambda dans un bureau de vote ([0,1])")
    proba = input()

    typecol = ""
    if typegen == "coalition":
        print("Entrez le mode dde coalition :")
        print("Entrez 'equilibre' afin que le groupe de candidats qui fraude se partagent equitablement les differrentes voix detournes aux autres candidats")
        print("Entrez 'concentre' afin que le groupe de candidats qui fraude se renvoie les differentes voix detournes a un seul d'entre eux")
        typecol = input()

    command = "python3 genPV/Gen_Pv_Files.py ~/Desktop "+typegen+" "+typecol+" "+proba+" ~/Desktop"
    print("Generation des pvs...", command)

    print("\033[37m")
    os.system(command)
    print("Les pvs sont generes !")


    #6 - Upload des pvs

    print("\033[32m")
    print ("---------------------------------------------------")
    print ("TELECHARGEMENT DES PROCES VERBAUX")
    print("Vous pouvez uploader les pv sur la plateforme de deux manieres")
    print(" -   manuellement depuis la plateforme http://206.189.210.30/eeyes/ ")
    print(" -   En utilisant une commande qui vous evite d'avoir a les uploader un a un !")
    print("Commencez par telecharger les pv generes dans votre machine.")
    print("\033[37m")
    print("utilisez pour cela la commande suivante dans un autre terminal : scp -r eeyes@206.189.210.30:/home/eeyes/Desktop/ ./EeyesData avec comme mot de passe 'eeyes2019'")
    print("\033[32m")

    print("-    Compilez le script EeyesData/sendPVs.py avec python3 pour envoyer automatiquement tous les pvs")
    print("-    Consultez la plateforme (index.html present dans le fichier eeyes.zip que vous aurez dezzipe) http://206.189.210.30/eeyes/ pour les uploader manuellement.")
    os.remove("~/Desktop/temp.pdf")

    #res = input()
    print("\033[37m")
    #if res == "yes":
     #   os.system("python3 sendPvs.py ~/Desktop http://localhost/uploadPv")

    print("Accedez a la plateforme et consultez les resultats !!")
    print("------------------------------------------------------")
    print("processus de test termine. Vous pouvez le recommencer, avec un nouveau fichier de configuration de session electorale.")
    print("Recommencer le test ? entrez 'yes' pour recommencer a partir de la generation du fichier de configuration, et 'no' pour fermer le systeme et eteindre la machine.")
    rep = input()
    os.system("rm -r ~/Desktop/.Jsons")
    os.system("rm -r ~/Desktop/Images")
    os.system("rm -r ~/Desktop/temp.pdf")
    

#7 - On eteind le reseau Eeyes
print("\033[32m")
print ("Test done ! Now we are going to shutdown the Eeyes Network.")
os.system("sh stopNetwork.sh")
