const modelsNamespace = 'org.eeyes.ressources'

//recupere sous forme de tableau toutes les sections de la hierachie sections
function getAllSections(liste){
  let seclist = []
  console.log("on recupere les section de la liste a "+liste.length+" elements")
  for (p=0;p<liste.length;p++){
    for (const s of getSectionsOf(liste[p])){
      console.log("on ajoute donc "+s)
      seclist.push(s);
    } 
  }
  return seclist
}

//on recupere toutes les sections d'un objet section qu'on renvoie en tableau
function getSectionsOf(item){
  let sl = []
  console.log("on renvoie deja "+item.name)
  sl.push(item.name)
  if (typeof item.sections != 'undefined'){
    for (l=0;l<item.sections.length;l++){
      var ti = l;
      console.log("on traite l'enfant numero "+l+" soit "+item.sections[l].name)
      for (const s of getSectionsOf(item.sections[l])){
        sl.push(s);
      } 
      l=ti;
      console.log("...le "+l+" ieme est fini pass au suivant")
    }
  }
  return sl
}

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
  pv.nombreElecteursInscrits = upload.nombreElecteursInscrits
  pv.nombreSuffrageEmi = upload.nombreSuffrageEmi
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
  
  console.log(bonRecap);
  
  //computer pv dans bonRecap
  for (i=0;i<bonRecap.resultats.length;i++){
    if (bonRecap.resultats[i].sectionName == upload.BV){
      bonRecap.resultats[i].nombreElecteursInscrits += pv.nombreElecteursInscrits
      bonRecap.resultats[i].nombreSuffrageEmi += pv.nombreSuffrageEmi
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
  let mere = getSectionParenteDe(upload.BV, bonRecap.sections, '');
  while (mere != ''){
    for (i=0;i<bonRecap.resultats.length;i++){
      if (bonRecap.resultats[i].sectionName == mere){
        bonRecap.resultats[i].nombreElecteursInscrits += pv.nombreElecteursInscrits
        bonRecap.resultats[i].nombreSuffrageEmi += pv.nombreSuffrageEmi
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


/**
 * Cette transaction enregistre le nouveau pv parmis les pv, puis met à jours le RecapPv correspondant
 * @param {org.eeyes.ressources.InitSE} data  Les donnnées uploadé, soit le nouveau pv
 * @transaction
 */
async function InitSE(data) {
  	
  /** Creation des participants (candidats) **/
  const authorReg = await getParticipantRegistry(modelsNamespace + '.Author')
  const factory = getFactory()

  
  //on ajoute ORGANISM et AUTHENTIC a la liste des participants pour qu'on cree son author et son recap pv
  data.candidates.push("ORGANISM");
  data.candidates.push("AUTHENTIC");
  //on cree donc les participant, organism en etant un aussi
  console.log("creation des authors:")
  for (j=0;j<data.candidates.length;j++){
    let pv = factory.newResource(modelsNamespace, 'Author', data.candidates[j])
    console.log("on cree "+pv.name)
    await authorReg.add(pv)
  }
  
  
  
  /** Creation des recapPV **/
  console.log("creation des recap PV:")
  const rpReg = await getAssetRegistry(modelsNamespace + '.RecapPV')
  for (j=0;j<data.candidates.length;j++){
    let rpv = factory.newResource(modelsNamespace, 'RecapPV', data.candidates[j])
    console.log("creation du recap PV de "+data.candidates[j])
    //info
    rpv.PVs = 0

    rpv.session = factory.newConcept(modelsNamespace, 'SessionInfo');//pour creer une instance de concept parreil pour une cle etrangere--------
    rpv.session.title = data.title
    rpv.session.start = data.start
    rpv.session.end = data.end
    rpv.session.seEndDate = data.seEndDate
    rpv.session.candidates = data.candidates
    rpv.session.currentBoss = data.currentBoss
    rpv.session.organism = data.organism
    rpv.session.bvs = data.bvs
    
    //on met le author scrutateur//utiliser le factory pour une cle etrangere--------
    console.log("on met la cle etrangere scrutateur...")
    
    const allCandidates = await authorReg.getAll();
    rpv.scrutateur = factory.newResource(modelsNamespace, 'Author',data.candidates[j]);
      
	console.log("on remplie les sections de ce recapPV...")
    //on rempli les sections
    rpv.sections = data.sections

    //on rempli les resultats NB:PTET FAUT USE LA FACON AVEC FACTORY, QUE DE CREER A CHAQUE FOIS LE JSON---------------
    rpv.resultats = []
    console.log("on remplie les resultats de ce recapPV...")
    listeSection = getAllSections(data.sections)
    console.log("all les sections : "+listeSection)
    for (const s of listeSection) {
      var sect = factory.newConcept(modelsNamespace, 'recapSection');
      sect.sectionName = s
      sect.nombreElecteursInscrits = 0
      sect.nombreSuffrageEmi = 0
      sect.candidateVoices = []

      //on rempli les candidates voices
      for (k=0;k<data.candidates.length;k++){
        if(data.candidates[k] == "ORGANISM") continue;
        if(data.candidates[k] == "AUTHENTIC") continue;
        let cv = factory.newConcept(modelsNamespace, 'Voices');
        cv.candidate = data.candidates[k]
        cv.voice = 0
        sect.candidateVoices.push(cv);
      }
      let cv = factory.newConcept(modelsNamespace, 'Voices');
      cv.candidate = "NULL"
      cv.voice = 0
      sect.candidateVoices.push(cv);
      
	  rpv.resultats.push(sect)
    }
    //on enregistre le nouveau rpv dans la BC
    console.log("on enregistre ce recapPV...")
    await rpReg.add(rpv)
  }
  //PK ON S'ARRETE AU PREMIER SCRUTATEUR ET ON NE CREE PAS LES RECAPPV DES AUTRES ???
  //PAS DE CANDIDATE VOICE POUR ORGANIZSM
  //les resultats ne prennent qu'une descendance des sections et non toutes...
}
    
//TODO
/*
- apprendre a deployer tout ceci sur un vrai reseau, et plus sur le playground.. ceci pour pouvoir ecrire le script qui cree automatiquement les assets

- script de creation et configuration des asset (installation de la SE) qui prend en entree le fichier SE-config.json et cree tous les asset et participants, de sorte que à la fin on attende plus que les transactions d'ajout de pvs.
- L'api de questionnement de la BC. Pour cela on pourra creer des transactions qui prennent en entree la question et donne en sortie le resultat, qui peut etre les pvs de tel candidats, de tel BV ou section, ou meme les recapPVs...
	- pv de scrutateur
    - pvs de candidats
    - pvs de section
    - pv de BV
- inserer dans recapPV les infos de la variable session dans RecapPV a l'initialisation de la se JUSTE
- gerer les nombre d'inscrits et de votant dans un bv JUSTE
*/