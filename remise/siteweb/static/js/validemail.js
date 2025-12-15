
"use strict";

// Validation de mail lors de la création de compte

function stopsubmit(event){
    event.preventDefault();
}

async function ValidateMail(mail){

    let compteForm = document.getElementById("aForm");

    compteForm.addEventListener("submit", () => stopsubmit());

    const regex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;

    const url = "/api/Compte/all_mail";

    const message = document.getElementById("message-mail");

    message.classList.remove("hidden");

    const mails = await envoyerRequeteAjax(url, "get", null, null);
    
    if(regex.test(mail.value)){

        if(mails.includes(mail.value)){
            message.textContent = "Ce mail existe déjà."
            message.classList.add("erreur")
        }
        else{
            message.textContent = "Ce mail est disponible."
            message.classList.add("valide")

            if(regex.test(mail.value)){
                compteForm.removeEventListener("submit", () => stopsubmit());
            }
        }
    }
    else{
        return;
    }    
}

function initialize(){
    let mail = document.getElementById("mail")
    mail.addEventListener("blur", () => ValidateMail(mail));
}

window.addEventListener("load", initialize);