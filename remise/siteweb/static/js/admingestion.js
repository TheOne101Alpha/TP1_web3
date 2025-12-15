
"use strict";
const filtre = document.getElementById("recherche");
function ajouter(){
    window.location.href = "/compte/creation";
}

async function suppression(button){
    const id = button.dataset.UserId;
    const url = '/api/compte/supprimer/' + id;

    const reponse = await envoyerRequeteAjax(url, 'GET');

    if(reponse){
        affichage();
        return;
    }

}


async function affichage(){
    const url = "/api/compte/all";
    const contenant = document.getElementById("compte_liste");
    contenant.replaceChildren();

    const comptes =  await envoyerRequeteAjax(url, "GET");

    for(let i = 0; i < comptes.length; i++){
        let divcontainer = document.createElement('div');
        divcontainer.classList.add('row', 'justify-content-around', 'text-center', 'm-1');

        let div1 = document.createElement("div");
        div1.classList.add("col-3", "border", "border-black");
        div1.textContent = comptes[i]['nom'];

        let div2 = document.createElement("div");
        div2.classList.add("col-3", "border", "border-black");
        div2.textContent = comptes[i]['role'];

        let div3 = document.createElement('div');
        let btn = document.createElement('button');
        btn.dataset.UserId = comptes[i]['id_compte']
        btn.textContent = "Supprimer";
        btn.classList.add('w-100', 'h-100');
        btn.addEventListener('click', () => suppression(btn));
        div3.classList.add("col-3");
        div3.append(btn);

        divcontainer.append(div1);
        divcontainer.append(div2);
        divcontainer.append(div3); 
        
        contenant.append(divcontainer);
    }

}

async function recherche(){
    const url = "/api/compte/all";
    const data =  await envoyerRequeteAjax(url, "GET");

    let aChercher = filtre.value.toLowerCase();

    if(aChercher.length > 4){
        const suggest = data.filter(item => item.nom.toLowerCase().includes(aChercher));
        const contenant = document.getElementById("compte_liste");
        contenant.replaceChildren();
        for(let i = 0; i < suggest.length; i++){
            let divcontainer = document.createElement('div');
            divcontainer.classList.add('row', 'justify-content-around', 'text-center', 'm-1');

            let div1 = document.createElement("div");
            div1.classList.add("col-3", "border", "border-black");
            div1.textContent = suggest[i]['nom'];

            let div2 = document.createElement("div");
            div2.classList.add("col-3", "border", "border-black");
            div2.textContent = suggest[i]['role'];  
            let div3 = document.createElement('div');
            let btn = document.createElement('button');
            btn.dataset.UserId = suggest[i]['id_compte']
            btn.textContent = "Supprimer";
            btn.classList.add('w-100', 'h-100');
            btn.addEventListener('click', () => suppression(btn));
            div3.classList.add("col-3");
            div3.append(btn);

            divcontainer.append(div1);
            divcontainer.append(div2);
            divcontainer.append(div3); 
            
            contenant.append(divcontainer);
        }
    }
    else if(aChercher.length === 0){
        affichage();
    }
    
}

// initialisation des ecouteurs d'évenements
function initialize(){
    const contenant = document.getElementById("compte_liste");
    let ajouterbtn = document.getElementById("ajouter");
    ajouterbtn.addEventListener("click", () => ajouter());
    affichage()
    filtre.addEventListener("input", recherche);
}

window.addEventListener("load", initialize);





