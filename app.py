"""TP2 WEB"""

import re
import os
import logging
from dotenv import load_dotenv
from flask import Flask, render_template, request, abort, redirect, session
from datetime import datetime
from modules.compte import bp_compte
from modules.api import bp_api
from modules.gestion_services import bp_gestion_services


if not os.getenv('BD_Utilisateur'):
    load_dotenv('.env')


reg_html = re.compile(r"(<(.*)>.*?|<(.*) />)")

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
app.register_blueprint(bp_compte, url_prefix = '/compte')
app.register_blueprint(bp_gestion_services, url_prefix = '/gestion_services')
app.register_blueprint(bp_api, url_prefix = '/api')

app.secret_key = os.getenv('Secret_Key')

@app.route('/')
def base():
    """Affiche la page d'acceuil du site"""
    return render_template('acceuil.jinja',  titre_page = "Acceuil", langue = "fr_CA")



@app.errorhandler(400)
def gestion400(e):
    """Gere le code 400"""
    return render_template("erreur.jinja", message = e.description), 400

@app.errorhandler(404)
def gestion404(e):
    """Gere le code 404"""
    chemin = request.path
    if chemin == "/details":
        return render_template("erreur.jinja", message = e.description), 404
    if chemin == "/changement":
        return render_template("erreur.jinja", message = e.description), 404
    return render_template("erreur.jinja", message = e.description), 404

@app.errorhandler(500)
def gestion500(e):
    """Gere le code 500"""
    return render_template("erreur.jinja", message = "Désoler, nous avons une " \
    "erreurs au niveau du server"), 500

if __name__ == "__main__":
    app.run()
