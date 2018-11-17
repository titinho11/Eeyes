const modelsNamespace = 'org.eeyes.ressources'

function getSectionParenteDe(section, liste, parnt){
  var parent = parnt;//mis pour le preview
  
  //getSectionParenteDe(upload.sectionName, bonRecap.sections);
  for (const s of liste) {
    if (s.name == section) {
      return parent;
    }
    else if (typeof s.sections != 'undefined') {
      var data = getSectionParenteDe(section, s.sections, s.name);
      if (data!='') return (data=='-')? s.name:data;
      //probleme de arrrivé au fond d une branche, comment
      //faire pour conseerver la recursivite ?
    }
    else if (typeof s.sections == 'undefined') {
        //return '';
    }
  }
  return '';
}

/**
 * Cette transaction enregistre le nouveau pv parmis les pv, puis met à jours le RecapPv correspondant
 * @param {org.eeyes.ressources.ComputePV} upload  Les donnnées uploadé, soit le nouveau pv
 * @transaction
 */
async function uploadPV(upload) {
  	
  /** Creation du PV dans le registre **/
  const pvRegistry = await getAssetRegistry(modelsNamespace + '.PV')
  const factory = getFactory()
  const pv = factory.newResource(modelsNamespace, 'PV', upload.code)
  pv.BV = upload.BV
  pv.sectionName = upload.sectionName
  pv.publishedDate = upload.publishedDate
  pv.candidateVoices = upload.candidateVoices
  pv.scrutateur = upload.scrutateur
  await pvRegistry.add(pv)

  /** MAJ du recapPV correspondant dans le registre **/
  //récupération du bon recapPV
  const recapPvRegistry = await getAssetRegistry(modelsNamespace + '.RecapPV')
  var bonRecap;
  const allRecapPV = await recapPvRegistry.getAll();
  for (const asset of allRecapPV) {
    if (asset.author_name == upload.scrutateur.name){
      bonRecap = asset;
      break;
    }
  }
  
  /*
  2- resoudre le pb de bureau de vote pour qu'on puisse aussi avoir les resultats par BV
  3- tenir compte des author vraipv et elecam
  4- tenir compte des voies du null
  */
  console.log(bonRecap);
  
  //computer pv dans bonRecap
  for (i=0;i<bonRecap.resultats.length;i++){
    if (bonRecap.resultats[i].sectionName == upload.sectionName){
      for (j=0;j<bonRecap.resultats[i].candidateVoices.length;j++){
        //bonRecap.resultats[i].candidateVoices
        for (k=0;k<upload.candidateVoices.length;k++){
          if (upload.candidateVoices[k].candidate == bonRecap.resultats[i].candidateVoices[j].candidate){
            bonRecap.resultats[i].candidateVoices[j].voice += upload.candidateVoices[k].voice;
            break;
          }
        }
      }
    }
  }
  
  //on met a jour le nombre de pv pris en consideration dans recapPV
  bonRecap.PVs +=1;
   
  //MAJ des resultats des sections parentes dans bonRecap
  let mere = getSectionParenteDe(upload.sectionName, bonRecap.sections, '');
  while (mere != ''){
    for (i=0;i<bonRecap.resultats.length;i++){
      if (bonRecap.resultats[i].sectionName == mere){
        for (j=0;j<bonRecap.resultats[i].candidateVoices.length;j++){
          for (k=0;k<upload.candidateVoices.length;k++){
            if (upload.candidateVoices[k].candidate == bonRecap.resultats[i].candidateVoices[j].candidate){
              bonRecap.resultats[i].candidateVoices[j].voice += upload.candidateVoices[k].voice;
              break;
            }
          }
        }
      }
    }
    mere = getSectionParenteDe(mere, bonRecap.sections, '');
  }

  //sauvegarder la MAJ
  await recapPvRegistry.update(bonRecap);
}
    
//TODO
/*
- apprendre a deployer tout ceci sur un vrai reseau, et plus sur le playground.. ceci pour pouvoir ecrire le script qui cree automatiquement les assets
- choisir et donner à francine les format de sorties, afin que francine puisse deja utiliser ces variables.
	- un pv
    - un tableau de pvs
    - un recap PV
    - un tableau de recapPV
- script de creation et configuration des asset (installation de la SE) qui prend en entree le fichier SE-config.json et cree tous les asset et participants, de sorte que à la fin on attende plus que les transactions d'ajout de pvs.
- L'api de questionnement de la BC. Pour cela on pourra creer des transactions qui prennent en entree la question et donne en sortie le resultat, qui peut etre les pvs de tel candidats, de tel BV ou section, ou meme les recapPVs...
	- pv de scrutateur
    - pvs de candidats
    - pvs de section
    - pv de BV
*/