import re
from datetime import datetime
from flask import Flask, render_template, request, abort, redirect, Blueprint, session, url_for, flash, jsonify, current_app as app
import bd

bp_compte = Blueprint('compte', __name__)



@bp_compte.route('/<int:id_compte>')
def index(id_compte):
    """Affiche les services postés par un utilisateur"""
    app.logger.debug("L'utilisateur demande ses services")
    if 'id' not in session:
        app.logger.info("L'utilisateur n'est pas connecté, redirection vers la page de connexion")
        return redirect('/compte/connexion')

    if not bd.id_exist(id_compte):
        app.logger.debug("L'utilisateur n'existe pas dans la base de données, abort 404")
        return abort(404, 'utilisateur inexistant')

    services = bd.get_services_compte(id_compte)
    app.logger.debug(f"L'utilisateur {id_compte} a {len(services)} services")
    return render_template('compte/services.jinja', lesservices=services)

@bp_compte.route('/connexion', methods=['GET', 'POST'])
def authen():
    """Affiche la page d'authentification"""
    nom = request.form.get('nom', type=str, default='')
    mdp = bd.hacher_mdp(request.form.get('mdp', type=str, default=''))

    if request.method == 'POST':
        app.logger.debug(f"Authentification de l'utilisateur {nom}")

        app.logger.debug("Vérification des informations dans la base de données")
        compte = bd.get_compte(nom, mdp)
        # si aucun compte ne reviens, on retourne sur la même page
        if not compte:
            flash('Connexion refusé')
            app.logger.debug("Les informations sont incorrectes")
            return render_template('compte/authentifier.jinja')
        #sinon la session est donnée à la personne
        app.logger.debug("Connexion réussie, création de la session")
        session.clear()
        session.permanent = True
        session['id'] = compte['id_compte']
        session['role'] = compte['role']
        session['credit'] = compte['credit']
        app.logger.debug(f"Session créée: {session}")
        return redirect('/', code=302)
    app.logger.debug("Affichage de la page d'authentification")
    return render_template('compte/authentifier.jinja')

@bp_compte.route('/deconnexion')
def deconnexion():
    """Deconnecte l'utilisateur et supprime la session"""
    app.logger.debug(f"Déconnexion de l'utilisateur {session.get('id')}")
    session.clear()
    return redirect('/')

@bp_compte.route('/creation', methods=['GET', 'POST'])
def creation():
    """Affiche la page de création de compte"""
    if request.method == 'POST':
        app.logger.debug("Création de compte demandée")
        nom = request.form.get('mail', type=str)
        mdp = request.form.get('mdp', type=str)
        mdp_hach = bd.hacher_mdp(mdp)
        role = request.form.get('role', type=str)

        valide = True

        if not nom or len(nom) < 8 or not is_valideMAIL(nom):
            flash('le mail est invalide', 'error')
            app.logger.debug("Le mail est invalide")
            valide = False

        if not mdp or len(mdp) < 8 or not is_valideMDP(mdp):
            flash('le mot de passe est invalide (1 majuscule, 1 minuscule, des chiffres)', 'error')
            app.logger.debug("Le mot de passe est invalide")
            valide = False
            
        if not valide:
            app.logger.debug("Les informations sont invalides, retour à la page de création")
            return render_template('compte/creation.jinja')

        app.logger.debug("Les informations sont valides, ajout du compte à la base de données")
        bd.add_compte(nom,mdp_hach,role)
        compte = bd.get_compte(nom, mdp_hach)

        app.logger.debug("Compte créé avec succès, création de la session")
        session.clear()
        session.permanent = True
        session["id"] = compte["id_compte"]
        session["role"] = role
        session["credit"] = compte["credit"]
        return redirect('/', code=302)
    
    app.logger.debug("Affichage de la page de création de compte")
    return render_template('compte/creation.jinja')

@bp_compte.route("/liste")
def liste():
    """Affiche tous les utilisateurs si l'utilisateur a le bon role"""
    app.logger.info("Affichage de la liste des utilisateurs pour l'administrateur")
    if session.get('role', default='') != 'admin':
        app.logger.warning("L'utilisateur n'a pas les droits d'accès, abort 401")
        abort(401, 'Vous ne pouvez pas faire ces modifications')
    app.logger.debug("Récupération des utilisateurs dans la base de données")
    comptes = bd.get_comptes()
    return render_template('compte/liste.jinja', lescomptes=comptes)

def is_valideMDP(chaine):
    """check si la chaine en entré respecte le paterne d'un mot de passe"""
    paterne = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$'
    return bool(re.match(paterne, chaine))

def is_valideMAIL(chaine):
    """check si la chaine en entré respecte le paterne d'un mail"""
    paterne = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return bool(re.match(paterne, chaine))
