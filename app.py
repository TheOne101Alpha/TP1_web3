"""TP2 WEB"""

import re
from datetime import datetime
from flask import Flask, render_template, request, abort, redirect
import bd

from gestion_services import bp_gestion_services





reg_html = re.compile(r"(<(.*)>.*?|<(.*) />)")

app = Flask(__name__)
app.register_blueprint(bp_gestion_services, url_prefix='/gestion_services')


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

@app.route("/details")
def details():
    """affiche la page de détail"""
    retour = []

    identifiant = request.args.get('id', type=int)

    if not identifiant:
        abort(400, "parametre id manquant")

    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            curseur.execute('SELECT cat.nom_categorie, ser.date_creation, ' \
            'ser.titre, ser.actif, ser.description, ser.cout,' \
            ' ser.localisation FROM services ser INNER JOIN' \
            ' categories cat ON cat.id_categorie = ser.id_categorie ' \
            'WHERE ser.id_service =%(id)s', {'id': identifiant})
            retour = curseur.fetchone()
            if not retour:
                abort(404, "details d'un service inexistant")

            return render_template("details.jinja", titre_page = "Détails",
                                    item = retour, id_change = identifiant)



@app.route("/changement", methods=['GET', 'POST'])
def changement():
    """affichage de changement ou ajout de services"""

    categories = []

    v_nom = ""
    v_local=""
    v_descr=""

    nom = request.form.get("nom_service","")
    localisation = request.form.get("localisation_service","")
    description = request.form.get("description_service","")
    actif = request.form.get("actif_service", 0, type=int)
    cout = request.form.get('cout', 0, type=float)

    identifiant = request.args.get('id', type=int)

    if request.method == 'POST':
        if reg_html.fullmatch(nom) or len(nom) < 1 or len(nom) > 50:
            v_nom = "is-invalid"
        if reg_html.fullmatch(localisation) or len(localisation) < 5 or len(localisation) > 50:
            v_local = "is-invalid"
        if reg_html.fullmatch(description) or len(description) < 5 or len(description) > 2000:
            v_descr = "is-invalid"

        if v_nom or v_local or v_descr:
            # si un des champs est faux
            # retourne sur la même page
            return render_template("changement.jinja", titre_page= "changement",
                                   valide_nom = v_nom, valide_localisation = v_local,
                                     valide_description = v_descr)
        # Sinon ajoute les données à la bd à l'aide de update
        date = datetime.now()
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute(
                    'UPDATE services SET titre= %(letitre)s, description= %(ladescription)s, ' \
                    'localisation= %(lalocalisation)s,date_creation= %(ladate)s' \
                    ', actif= %(si_actif)s,cout= %(lecout)s WHERE id_service = %(ident)s',
                    {
                        'letitre': nom,
                        'ladescription': description,
                        'lalocalisation': localisation,
                        'si_actif': actif,
                        'lecout': cout,
                        'ladate': date,
                        'ident': identifiant
                    }
                )
                conn.commit()
                return redirect("/merci_modif", code=303)
    if not identifiant:
        abort(400, "le parametre id est manquant")

    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            curseur.execute("SELECT id_categorie,nom_categorie FROM categories")
            categories= curseur.fetchall()
            curseur.execute('SELECT cat.nom_categorie, ser.date_creation,' \
            ' ser.titre, ser.actif, ser.description, ser.cout, ' \
            'ser.localisation FROM services ser INNER JOIN categories cat ' \
            'ON cat.id_categorie = ser.id_categorie WHERE ' \
            'ser.id_service =%(id)s', {'id': identifiant})
            leservice = curseur.fetchone()
            if not leservice:
                abort(404, "le service à modifier n'existe pas")
            return render_template("changement.jinja",titre_page = "Modification service",
                                    service=leservice, liste_categorie = categories)

@app.route("/ajout", methods=['GET', 'POST'])
def ajout():
    """ajoute un nouveau service dans la bd"""
    categories = []

    v_nom = ""
    v_local=""
    v_descr=""

    nom = request.form.get("nom_service", default= "")
    localisation = request.form.get("localisation_service", default= "")
    description = request.form.get("description_service", default= "")
    categorie = request.form.get("choix_categorie", default=None, type=int)
    actif = request.form.get("actif_service", default= 0, type=int)
    cout = request.form.get('cout', default=0, type=int)
    if request.method == 'POST':
        if reg_html.fullmatch(nom) or len(nom) < 1 or len(nom) > 50:
            v_nom = "is-invalid"
        if reg_html.fullmatch(localisation) or len(localisation) < 5 or len(localisation) > 50:
            v_local = "is-invalid"
        if reg_html.fullmatch(description) or len(description) < 5 or len(description) > 2000:
            v_descr = "is-invalid"

        if v_nom or v_local or v_descr:
            # si un des champs est faux
            # retourne sur la même page
            return render_template("ajout.jinja", titre_page= "ajout",
                                   valide_nom = v_nom, valide_localisation = v_local,
                                     valide_description = v_descr, titre = nom,
                                     local=localisation, description=description,cout = cout)
        # Sinon ajoute les données à la bd à l'aide de INSERT
        date = datetime.now()
        with bd.creer_connexion() as conn:
            with conn.get_curseur() as curseur:
                curseur.execute(
                    'INSERT INTO services VALUES (NULL,%(categorie_id)s,%(letitre)s,'
                    '%(ladescription)s,%(lalocalisation)s,%(ladate)s,'
                    '%(si_actif)s,%(lecout)s, NULL)',
                    {
                        'letitre': nom,
                        'ladescription': description,
                        'lalocalisation': localisation,
                        'ladate': date,
                        'categorie_id': categorie,
                        'si_actif': actif,
                        'lecout': cout,
                    }
                )
                conn.commit()
                return redirect("/merci_modif", code=303)
    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            curseur.execute("SELECT id_categorie, nom_categorie FROM categories")
            categories= curseur.fetchall()
            return render_template("ajout.jinja",titre_page = "ajout service",
                                    liste_categorie = categories)

@app.route("/services")
def services():
    """Affiche tous les services dans la base de données"""
    retour = []
    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            curseur.execute("SELECT id_service, (SELECT nom_categorie FROM " \
            "`categories` WHERE categories.id_categorie " \
            "= services.id_categorie), titre, localisation, " \
            "description FROM `services` ORDER BY services.date_creation")
            retour = curseur.fetchall()
    return render_template('services.jinja',titre_page = "Services", lesservices=retour)

@app.route("/merci_modif")
def merci():
    """affiche un message si un service est modifié"""
    return render_template("merci.jinja", message = "modifier", titre_page = "ajout reussi")

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
