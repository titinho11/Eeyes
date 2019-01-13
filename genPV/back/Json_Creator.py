import json


def create_pv_json(pv, location_files):
    content = {'$class': "org.eeyes.ressources.ComputePV", 'code': "{}:{}".format(pv.bv.father.name, pv.owner),
               'BV': pv.bv.name, 'sectionName': pv.bv.father.name, 'nombreElecteursInscrits': pv.bv.register_num,
               'nombreSuffrageEmi': pv.bv.voters_num, 'candidateVoices': []}

    for r in pv.result:
        temp = {'$class': 'org.eeyes.ressources.Voices', 'candidate': r, 'voice': pv.result[r]}
        content['candidateVoices'].append(temp)
    content['scrutateur'] = "resource:org.eeyes.ressources.Author#{}".format(pv.owner)

    with open('{}/.Jsons/{}/{}.json'.format(location_files, pv.owner.replace(' ', '_'), pv.bv.name.replace(' ', '_')), 'w',
              encoding='utf-8') as outfile:
        json.dump(content, outfile, indent=4, ensure_ascii=False)