"use strict";
const list = document.getElementById('liste');

let nombre = 0;
let maxservice = 0;

async function ajouterItemListe(taux = 6){
    const services = await envoyerRequeteAjax('/api/services/all_details', 'GET');
    maxservice = services.length;
    for(let i = 0; i< taux && nombre < maxservice; i++){
        let contenant = document.createElement('div');
        contenant.classList.add('card', 'taille', 'col-md-6');
        
        let body = document.createElement('div');
        body.classList.add('card-body');

        let titre = document.createElement('p');
        titre.classList.add('h2', 'card-title');
        titre.textContent = services[nombre]['titre'];

        let img = document.createElement('img');
        img.classList.add('card-text');
        img.src = '/static/placeholder.png';
        img.alt = 'image placeholder';

        let information = document.createElement('p');
        information.classList.add('card-text');
        information.innerHTML = `${services[nombre]['nom_categorie']} <br> ${services[nombre]['description']} <br> localisation: ${services[nombre]['localisation']}` 

        let lien = document.createElement('a');
        lien.href = `details/${services[nombre]['id_service']}`;
        lien.classList.add('text-decoration-none', 'w-25');

        let info = document.createElement('div');
        info.classList.add('bg-info', 'text-white', 'h3', 'inline-text');
        info.textContent = "Voir plus";


        lien.append(info);


        body.append(titre, img, information, lien);
        contenant.append(body);
        list.append(contenant);

        nombre ++;
    }
}




function gererDefilement() {
    if ( ((window.innerHeight + window.scrollY) >= 0.95 * document.body.offsetHeight) && (nombre < maxservice)) {
        ajouterItemListe(3);
    }
    if ((nombre >= maxservice)) {
        window.removeEventListener("scroll", gererDefilement)
    }
}

function initialisation() {
    window.addEventListener('scroll', gererDefilement);
    list.removechildren;
    ajouterItemListe(6);
}

window.addEventListener('load', initialisation);