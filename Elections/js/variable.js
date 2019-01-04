/***Kateu Firmin*/

var res = [];
lien = "http://localhost:3000/api/RecapPV";
$.ajax({
    url: lien,
    type: "GET",
    async: false,
    complete: function(dat){
			console.log(dat)
			res=dat.responseJSON;
    }
});

var data = res;

/**Fin de l'import */
