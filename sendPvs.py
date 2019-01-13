import requests
import json
from os import listdir
import sys
#from os.path import isfile, join


path = sys.argv[1]+"/.Jsons"
lien = "http://localhost:3000/api/ComputePV"#sys.argv[2]

dossiers = [f for f in listdir(path)]
#print (fichiers)

for dossier in dossiers:
    print("Envoi des PVs du candidat "+dossier)
    path2 = path+"/"+dossier
    fichiers = [f for f in listdir(path2) if f.endswith('.json')]

    for fichier in fichiers:
        print("Envoi du procès verbal du bureau de vote : "+fichier.strip('.json')+" ... ", end='')
        data = json.loads(open(path2+"/"+fichier).read())
        #data["titre"] = fichier
        data["publishedDate"] = "2018-11-14T07:20:14.404Z"
        r = requests.post(lien, json=data)
        print(r)#print("fait !")
    print("\n")
        
