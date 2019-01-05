from Gen_Pv import main
from Image_Creator import create_pv_image
from Json_Creator import create_pv_json
import sys

if sys.argv[2] == 'coalition':
    list_bureau_vote = main(sys.argv[1], sys.argv[5], type_generation= sys.argv[2], type_coalition = sys.argv[3], probabilite_possesion = float(sys.argv[4]))
    location_files = sys.argv[5]
else:
    list_bureau_vote = main(sys.argv[1], sys.argv[4], sys.argv[2], probabilite_possesion = float(sys.argv[3]))
    location_files = sys.argv[4]
"""create_pv_image(list_bureau_vote[0].pVs[0], location_files)
create_pv_json(list_bureau_vote[0].pVs[0], location_files)"""
for bv in list_bureau_vote:
    for pv in bv.pVs:
        sys.stdout.write("Generation de "+str(pv)+"...")
        create_pv_image(pv, location_files)
        create_pv_json(pv, location_files)
        sys.stdout.write("Fait.\n")
