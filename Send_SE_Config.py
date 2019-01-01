import requests
import sys
import json

url_api = "http://localhost:3000/api/InitSE"

file = open("{}/SE-config.json".format(sys.argv[1]), encoding='utf-8').read()
datas = json.loads(file)

datas["$class"] =  "org.eeyes.ressources.InitSE"
datas["seEndDate"] = datas["SE end date"]
del(datas["SE end date"])
datas["candidates"] = datas["authors"]
del(datas["authors"])
del(datas["country"])
del(datas["voters registered by BV"])
datas["bvs"] = datas["BVs"]
del(datas["BVs"])

"""print("******************************")
print(datas)
print("******************************")"""

response = requests.post(url=url_api, json=datas).json()

print(response)
