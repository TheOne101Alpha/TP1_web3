"use strict";

// Appel asynchrone et affichage des suggestions
const suggestion = document.querySelector(".sug");
const input = document.getElementById("input");
async function suggestions(){
    let text = input.value;

    suggestion.innerHTML = '';

    let controlleur = null;
    let url = "/api/services/all"

    if(text === "" || text.length< 3){
        suggestion.classList.add("hidden");
        return;
    }

    suggestion.classList.remove("hidden");
    try{
        const data = await envoyerRequeteAjax(url, "GET",null,controlleur);

        const ul = document.createElement("ul");
        const suggest = data.filter(item => item.titre.toLowerCase().includes(text.toLowerCase()));

        for(let i = 0; i < suggest.length; i++){
            const li = document.createElement("li");
            const lien = document.createElement("a");
            lien.href = "/gestion_services/details/" + suggest[i].id;
            lien.textContent = suggest[i].titre;
            lien.dataset.id_service = suggest[i].id;
            lien.dataset.titre = suggest[i].titre;
            lien.addEventListener("click", function(){
                let service = {id: this.dataset.id_service,
                               titre: this.dataset.titre};
                StockageSuggestions(service);
            });
            li.append(lien);
            ul.appendChild(li);
        }
        suggestion.appendChild(ul);
    }
    catch(err){
        console.log(err);
        console.log(err.message);
    }
}

async function UpdateAcceuil(){
    const url = "/api/services/all_details";
    const affichage = document.getElementById("acceuil_liste");
    affichage.innerHTML = '';
    const data = await envoyerRequeteAjax(url, "GET", null, null);
    let nb = 0;
    while(nb < 5 && nb < data.length){
        let contenant = document.createElement('div');
        contenant.classList.add('card', 'taille', 'col-md-6');
        
        let body = document.createElement('div');
        body.classList.add('card-body');

        let titre = document.createElement('p');
        titre.classList.add('h2', 'card-title');
        titre.textContent = data[nb]['titre'];

        let img = document.createElement('img');
        img.classList.add('card-text');
        img.src = '/static/placeholder.png';
        img.alt = 'image placeholder';

        let information = document.createElement('p');
        information.classList.add('card-text');
        information.innerHTML = `${data[nb]['nom_categorie']} <br> ${data[nb]['description']} <br> localisation: ${data[nb]['localisation']}` 

        let lien = document.createElement('a');
        lien.href = `details/${data[nb]['id_service']}`;
        lien.classList.add('text-decoration-none', 'w-25');

        let info = document.createElement('div');
        info.classList.add('bg-info', 'text-white', 'h3', 'inline-text');
        info.textContent = "Voir plus";


        lien.append(info);


        body.append(titre, img, information, lien);
        contenant.append(body);

        affichage.append(contenant);
        nb++;
    }
}

function StockageSuggestions(service){
    let tableau = JSON.parse(localStorage.getItem("suggestions"));

    if(!tableau){
        tableau = [];
        tableau.push(service);
        localStorage.setItem("suggestions", JSON.stringify(tableau));
        return;
    }

    if(!tableau.includes(service)){
        tableau.push(service);
        localStorage.setItem("suggestions", JSON.stringify(tableau));
        return;
    }
    return;
}


// initialisation des ecouteurs d'évenements
function initialize(){
    const input = document.getElementById("input");
    input.addEventListener("input", suggestions);
    UpdateAcceuil();
    setInterval(UpdateAcceuil, 5000);
}

window.addEventListener("load", initialize);





