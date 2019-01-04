import json
import sys
import math


def gen_children(level, children_num, name):
    if level > 1:
        collection = []
        for i in range(children_num):
            temp = {
                "$class": "org.eeyes.ressources.Section",
                "name": "{}_{}".format(name,i+1)
            }
            temp["sections"] = gen_children(level - 1, children_num, temp["name"])
            collection.append(temp)
        return collection
    else:
        collection = []
        for i in range(children_num):
            temp = {
                "$class": "org.eeyes.ressources.Section",
                "name": "{}_{}".format(name, i + 1)
            }
            collection.append(temp)
        return collection

tree_depth = int(sys.argv[1])
sub_sections_by_section = int(sys.argv[2])

tree = gen_children(tree_depth, sub_sections_by_section, "Section")

c = []
with open(sys.argv[11]) as my_file:
    for line in my_file:
        c.append(line.strip())

output = {
  "country": sys.argv[4],
  "title": sys.argv[5],
  "start": sys.argv[6],
  "end": sys.argv[7],
  "SE end date": sys.argv[8],
  "authors": c,
  "currentBoss": c[0],
  "organism": sys.argv[9],
  "BVs": int(math.pow(sub_sections_by_section, tree_depth)),
  "voters registered by BV": int(sys.argv[10]),
  "sections": tree
}

with open('{}/SE-config.json'.format(sys.argv[3]), 'w', encoding='utf-8') as outfile:
    json.dump(output, outfile, indent=4, ensure_ascii=False)