import re
from datetime import datetime
from flask import Flask, render_template, request, abort, redirect, Blueprint, session, url_for, flash
import bd

bp_compte = Blueprint('compte', __name__)



@bp_compte.route('/<int:id_compte>')
def index(id_compte):
    """Affiche les services postés par un utilisateur"""
    print(id_compte)
    if 'id' not in session:
        return redirect('/compte/connexion')

    if not bd.id_exist(id_compte):
        return abort(404, 'utilisateur inexistant')

    services = bd.get_services_compte(id_compte)
    print(services)
    return render_template('compte/services.jinja', lesservices=services)

@bp_compte.route('/connexion', methods=['GET', 'POST'])
def authen():
    """Affiche la page d'authentification"""
    nom = request.form.get('nom', type=str, default='')
    mdp = bd.hacher_mdp(request.form.get('mdp', type=str, default=''))

    print("Plain entered:", request.form.get('mdp'))
    print('the name: ' , request.form.get('nom'))
    print("Hash computed:", mdp)

    # if 'nom' not in session:
    #     return render_template('compte/authentifier.jinja')
    if request.method == 'POST':
        compte = bd.get_compte(nom, mdp)
        print(compte)
        # si aucun compte ne reviens, on retourne sur la même page
        if not compte:
            flash('Connexion refusé')
            print('un message est flash')
            return render_template('compte/authentifier.jinja')
        #sinon la session est donnée à la personne
        session.permanent = True
        session['id'] = compte['id_compte']
        session['role'] = compte['role']
        session['credit'] = compte['credit']
        print(session)
        return redirect('/', code=302)
    return render_template('compte/authentifier.jinja')

@bp_compte.route('/deconnexion')
def deconnexion():
    """Deconnecte l'utilisateur et supprime la session"""
    session.clear()
    return redirect('/')

@bp_compte.route('/creation', methods=['get', 'post'])
def creation():
    """Affiche la page de création de compte"""
    nom = request.form.get('mail', type=str)
    mdp = request.form.get('mdp', type=str)
    mdp_hach = bd.hacher_mdp(mdp)
    role = request.form.get('role', type=str)

    if request.method == 'POST':
        if not nom or len(nom) < 8 or is_valideMAIL(nom):
            flash('le MAIL est invalide', 'error')
            return render_template('compte/creation.jinja')

        if not mdp or len(mdp) < 8 or is_valideMDP(mdp):
            flash('le mot de passe est invalide (1 majuscule, 1 minuscule, des chiffres)', 'error')
            return render_template('compte/creation.jinja')

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


def is_valideMDP(chaine):
    """check si la cahine en entré respecte le paterne d'un mot de passe"""
    paterne = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$'
    return bool(re.match(paterne, chaine))

def is_valideMAIL(chaine):
    """check si la chaine en entré respecte le paterne d'un mail"""
    paterne = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return bool(re.match(paterne, chaine))
