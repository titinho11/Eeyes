from Gen_Pv import main
from Image_Creator import create_pv_image
from Json_Creator import create_pv_json
import sys

if sys.argv[1] == 'coalition':
    list_bureau_vote = main('SE-config.json', sys.argv[4], sys.argv[1], type_coalition = sys.argv[2], probabilite_possesion = float(sys.argv[3]))
    location_files = sys.argv[4]
else:
    list_bureau_vote = main('SE-config.json', sys.argv[3], sys.argv[1], probabilite_possesion = float(sys.argv[2]))
    location_files = sys.argv[3]
""""create_pv_image(list_bureau_vote[0].pVs[0])
create_pv_json(list_bureau_vote[0].pVs[0])"""
for bv in list_bureau_vote:
    for pv in bv.pVs:
        create_pv_image(pv, location_files)
        create_pv_json(pv, location_files)