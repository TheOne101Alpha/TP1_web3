"use strict";

const list = document.getElementById('liste');

async function affichageServicesUtilisateur(){
    const url = "/api/services/mes_services/" + list.dataset.id;
    console.log(url);
    console.log(list.dataset.id);
    list.innerHTML = '';
    const services = await envoyerRequeteAjax(url, 'GET');

    for(let i = 0; i < services.length; i++){
        let contenant = document.createElement('div');
        contenant.classList.add('card', 'taille', 'col-md-6');
        let body = document.createElement('div');
        body.classList.add('card-body');

        let titre = document.createElement('p');
        titre.classList.add('h2', 'card-title');
        titre.textContent = services[i]['titre'];
        let img = document.createElement('img');
        img.classList.add('card-text');
        img.src = '/static/placeholder.png';
        img.alt = 'image placeholder';
        let information = document.createElement('p');
        information.classList.add('card-text');
        information.innerHTML = `${services[i]['nom_categorie']} <br> ${services[i]['description']} <br> localisation: ${services[i]['localisation']}`
        let lienDetails = document.createElement('a');
        lienDetails.href = `../gestion_services/details/${services[i]['id_service']}`;
        lienDetails.classList.add('text-decoration-none', 'w-25', 'me-2');
        let infoDetails = document.createElement('div');
        infoDetails.classList.add('bg-info', 'text-white', 'h3', 'inline-text');
        infoDetails.textContent = "Détails du service";
        lienDetails.append(infoDetails);
        let buttonsupprimer = document.createElement('a');
        buttonsupprimer.dataset.serviceId = services[i]['id_service'];
        buttonsupprimer.addEventListener('click', function(){
            SupprimerService(buttonsupprimer.dataset.serviceId);
        })
        buttonsupprimer.classList.add('text-decoration-none', 'w-25', 'ms-2');
        let infoSupprimer = document.createElement('div');
        infoSupprimer.classList.add('bg-info', 'text-white', 'h3', 'inline-text');
        infoSupprimer.textContent = "Supprimer le service";
        buttonsupprimer.append(infoSupprimer);
        body.append(titre, img, information, lienDetails, buttonsupprimer);
        contenant.append(body);
        list.append(contenant);
    }
}

async function SupprimerService(id_service){
    const url = "/api/services/supprimer/" + id_service;
    console.log(id_service)
    const reponse = await envoyerRequeteAjax(url, 'GET', null, null);

    if(reponse){
        affichageServicesUtilisateur();
        return;
    }
}

window.addEventListener("load", async function(){
    await affichageServicesUtilisateur();
});