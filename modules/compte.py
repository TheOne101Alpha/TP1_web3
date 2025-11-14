import re
from datetime import datetime
from flask import Flask, render_template, request, abort, redirect, Blueprint, session, url_for, flash
import bd
import hashlib


def hacher_mdp(mdp_en_clair):
    """Prend un mot de passe en clair et lui applique une fonction de hachage"""
    return hashlib.sha512(mdp_en_clair.encode()).hexdigest()


bp_compte = Blueprint('compte', __name__)

bp_compte.route('/creation', methods=['get', 'post'])
def creation():
    """Affiche la page de création de compte"""

    nom = request.form.get('mail', type=str)
    mdp = request.form.get('mdp', type=str)
    mdp_hach = hacher_mdp(mdp)
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
            session["nom"] = nom
            session["role"] = role
            redirect('/', code=300)
    return render_template('compte/creation.jinja')

bp_compte.route("/liste")
def liste():
    """Affiche tous les utilisateurs si l'utilisateur a le bon role"""

    if session['role'] != 'admin':
        abort(401, 'Vous ne pouvez pas faire ces modifications')

    