import re
from datetime import datetime
from flask import Flask, render_template, request, abort, redirect, Blueprint, session, url_for, flash
import bd

bp_compte = Blueprint('compte', __name__)

@bp_compte.route('/', methods=['GET', 'POST'])
def authen():
    """Affiche la page d'authentification et l'index du bp compte"""
    nom = request.form.get('nom', type=str, default='')
    mdp = bd.hacher_mdp(request.form.get('mdp', type=str, default=''))

    if 'nom' not in session:
        return render_template('compte/authentifier.jinja')


    if request.method == 'POST':
        compte = bd.get_compte(nom, mdp)
        # si aucun compte ne reviens, on retourne sur la même page
        if not compte:
            flash('Connexion refusé')
            return render_template('compte/authentifier.jinja')
        
        #sinon la session est donnée à la personne
        session.permanent = True
        session['nom'] = compte['nom']
        session['role'] = compte['role']
        session['credit'] = compte['credit']
        return redirect('/', code=302)

    

@bp_compte.route('/creation', methods=['get', 'post'])
def creation():
    """Affiche la page de création de compte"""

    nom = request.form.get('mail', type=str)
    mdp = request.form.get('mdp', type=str)
    mdp_hach = bd.hacher_mdp(mdp)
    role = request.form.get('role', type=str)

    if request.method == 'POST':
        if not nom or len(nom) < 4:
            flash('le nom est invalide', 'warning')
            return url_for('creation')

        if not mdp or len(mdp) < 4:
            flash('le mot de passe est invalide', 'warning')
            return url_for('creation')

        compte = bd.get_compte(nom, mdp_hach)
        if not compte:
            bd.add_compte(nom,mdp_hach,role)
            session.clear()
            session.permanent = True
            session["nom"] = nom
            session["role"] = role
            redirect('/', code=302)
    return render_template('compte/creation.jinja')

@bp_compte.route("/liste")
def liste():
    """Affiche tous les utilisateurs si l'utilisateur a le bon role"""

    print('role : ' + session.get('role'))
    if session.get('role', default='') != 'admin':
        abort(401, 'Vous ne pouvez pas faire ces modifications')
    comptes = bd.get_comptes()
    return render_template('compte/liste.jinja', lescomptes=comptes)

@bp_compte.route("/suppression/<int:id>")
def suppr(id):
    """Supprime un compte et affiche la liste mis à jour"""
    if id > 0:
        bd.delete_compte(id)
        return render_template('compte/liste.jinja', lescomptes=bd.get_comptes())
    return abort(404)
