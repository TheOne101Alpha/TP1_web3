"""TP2 WEB"""

import re
from datetime import datetime
from flask import Flask, render_template, request, abort, redirect, session, flash
from modules.compte import bp_compte
import bd

from modules.gestion_services import bp_gestion_services





reg_html = re.compile(r"(<(.*)>.*?|<(.*) />)")

app = Flask(__name__)

app.register_blueprint(bp_compte, url_prefix = '/compte')
app.register_blueprint(bp_gestion_services, url_prefix = '/gestion_services')

app.secret_key = '6588ecc079c1f23d71a5f0f67ece4e7cf0cc8681df20e775ded64740cef3d462'

@app.route('/')
def base():
    """Affiche la page d'acceuil du site"""
    retour = []
    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            curseur.execute("SELECT cat.nom_categorie,ser.id_service," \
            " ser.titre, ser.description, ser.cout, ser.localisation " \
            "FROM services ser INNER JOIN categories cat ON " \
            "cat.id_categorie = ser.id_service ORDER BY ser.date_creation LIMIT 5")
            retour = curseur.fetchall()

    return render_template('acceuil.jinja',  titre_page = "Acceuil", langue = "fr_CA", items=retour)



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
