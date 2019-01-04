
/**Tableau qui garde les résultats cumulés de chaque candidat 
 * Il s'agit d'un tableau qui a le nombre de candidats lignes et 4 colonnes
 * la première colonne correspond au nom des candidats, la seconde à total des vrais suffrages
 * la troisième au total de l'organisme et la dernière au total des scrutateurs
*/

/**Import de la variable résultat */
NOTE: 

/*Chaque fois que l'on chargera le site, tu recevra le tableau ci. Maintenant tous les cliques qui se ferons dans le site pour charger les resultats
d'une section en particulier ou d'un candidat en particulier, tu aura deja les resultats totaux ci, du coups tu va juste extraire de ces resultats
ceux qui t'interresse, puis charger l'affichage correspondant. donc la consultation des resultats sera assez fluide, car il n'ya plus d'appels vers
le serveur. Ca veut aussi dire que tant que la page n'est pas reload (F5), les resultats ne sont pas à jours (car depuis le précedent chargement 
des pvs peuvent etre arrivés, sauf que il faut recharger la page pour faire un nouvel appel au serveur et recuperer les RecapPV à jours).
*/

/**Fin de l'import */

  data[0].session.candidates.pop();
  data[0].session.candidates.pop();
  data[0].session.candidates.push("NULL");
  console.log("tableau candidat")
  console.log(data[0].session.candidates);

/**Début calcul résultat final de chaque candidat */
/**Liste des candidats */
console.log("data...")
console.log(data);
nb=data[0].session.candidates.length;
//n est la taille du tableau resultats
results = new Array();
let n = data.length;
let etat = false;
//Initialisation des variables de PVs recus, Pvs attendus et Voix exprimés
let Pv_recu=0;
let Pv_attendu = 0;
let voix =0;
/**Initialisation du tableau qui contiendra le tableau des vrais résultats */
for(let a=0;a<4;a++){
    results[a]=new Array();  
}
for(let i=0;i<nb;i++){
    results[0][i]= data[0].session.candidates[i];
    //Organisme
    results[1][i]=0;
    //Majorité
    results[2][i]=0;
    //Vrai résultats
    results[3][i]=0;
}
function resultat_true_final(nom_auteur,index){
    //Stockage de la liste des grandes sections dont les resultats sont disponibles
    let test;
    voix=0;
    for(let i=0;i<n;i++){
        if (data[i].author_name == nom_auteur){
            etat=true; 
            test = i;  
            break;
        }
    }
    t= data[test].sections.length;
    m=data[test].resultats.length;
    l=data[test].resultats[0].candidateVoices.length;
    list_sec = new Array();
    for(let j=0;j<t;j++){
        list_sec[j]=data[test].sections[j].name;
    }
    if(etat){
        for(let j=0;j<t;j++){
            if(j!=0){
                Pv_recu+= data[test].PVs;
                Pv_attendu+=data[test].session.bvs;
            }
            for(let k=0;k<m;k++){
                if(data[test].resultats[k].sectionName == list_sec[j]){
                    voix += parseInt(data[test].resultats[k].nombreSuffrageEmi);
                    for(let p=0;p<l;p++){
                        for(let a=0;a<nb;a++){
                            if(data[test].resultats[k].candidateVoices[p].candidate==data[0].session.candidates[a]){
                                results[index][a]+= parseInt(data[test].resultats[k].candidateVoices[p].voice);
                                break;
                            }
                        }  
                    }
                    break;
                }
            }
        } 
    }
}
resultat_true_final(data[0].session.candidates[0],1);
resultat_true_final("ORGANISM",2);
resultat_true_final("AUTHENTIC",3);

{
    //Donut Dashboard
    //Construction de tableau de données
    let donut_data=new Array();
    let bar_data=new Array();
    for(let i=0;i<nb;i++){
       let str = {
           'label': "",
           'value': 0
       };
       let str1={
           'y':"",
           'a': 0,
           'b':0,
           'c':0
       };
       str['label'] = results[0][i].toString();
       str['value']= results[3][i];
       str1['y'] = str['label'];
       str1['a']=results[2][i];
       str1['b']=results[1][i];
       str1['c']=str['value'];
        donut_data[i] = str;
        bar_data[i]=str1;
    }
    $(function(){
        Morris.Donut({
    element: 'dashboard-donut-2',
    data: donut_data,
    colors: ['#33414E', '#1caf9a', '#FEA223','#7a4503','#1307ee'],
    resize: true
});

//Bar Dashboard
/* Bar dashboard chart */
Morris.Bar({
    element: 'dashboard-bar-2',
    data: bar_data,
    xkey: 'y',
    ykeys: ['a', 'b','c'],
    labels: ['Organisme', 'Majorité', 'Vrai'],
    barColors: ['#33414E', '#1caf9a', '#f19008'],
    gridTextSize: '10px',
    hideHover: true,
    resize: true,
    gridLineColor: '#E5E5E5'
});
    });
/* END Bar dashboard chart */
}
console.log(Pv_recu, Pv_attendu, voix);

//Initialisation des éléments d'en tête
document.getElementById('pv_recu').innerHTML = Pv_recu;
document.getElementById('pv_attendu').innerHTML = Pv_attendu;
document.getElementById('voix').innerHTML = voix;

