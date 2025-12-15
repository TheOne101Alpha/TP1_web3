"use strict";


const date = document.getElementById("service_date");
const lien = document.querySelector("#reserver");
const message = document.getElementById("message");

async function ButtonActif(){
    const url = '/api/reservation/check_date/' + lien.dataset.id_service;
    const reponse = await envoyerRequeteAjax(url, 'GET');

    if(reponse === true){
        lien.classList.remove('hidden');
    }
    else{
        lien.classList.add('hidden');
        message.classList.remove('hidden');
        message.textContent = "Service déjà réservé à cette date.";
    }
}

function initialize(){
    date.addEventListener("change", ButtonActif);
}

window.addEventListener("load", initialize);