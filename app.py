from flask import Flask, render_template, request, abort, redirect
import bd
import re





reg_html = re.compile(r"(<(.*)>.*?|<(.*) />)")

app = Flask(__name__)

@app.route('/')
def base():
    """Affiche la page d'acceuil du site"""
    retour = []
    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            curseur.execute("SELECT cat.nom_categorie,ser.id_service, ser.titre, ser.description, ser.cout, ser.localisation FROM services ser INNER JOIN categories cat ON cat.id_categorie = ser.id_service ORDER BY ser.date_creation LIMIT 5")
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
            curseur.execute('SELECT cat.nom_categorie, ser.date_creation, ser.titre, ser.actif, ser.description, ser.cout, ser.localisation FROM services ser INNER JOIN categories cat ON cat.id_categorie = ser.id_service WHERE ser.id_service =%(id)s', {'id': identifiant})
            retour = curseur.fetchone()
            if retour.rowcount == 0:
                abort(404, "details d'un service inexistant")

            return render_template("details.jinja", titre_page = "Détails", item = retour, id_change = identifiant)



@app.route("/changement", methods=['GET', 'POST'])
def changement():
    """affichage de changement ou ajout de services"""

    leservice = []
    categories = []

    v_nom = ""
    v_local=""
    v_descr=""

    identifiant = request.args.get('id', type=int)

    if request.method == 'POST':
        
        nom = request.form.get('nom_service')
        localisation = request.form.get('localisation_service')
        description = request.form.get('description_service')

        if reg_html.fullmatch(nom):
            v_nom = "is-invalid"
        if reg_html.fullmatch(localisation):
            v_local = "is-invalid"
        if reg_html.fullmatch(description):
            v_descr = "is-invalid"    
        if not v_nom and not v_local and not v_descr:
            return render_template("merci.jinja", titre_page= "Merci.jinja")
        return render_template(
            "changement.jinja",
            titre_page = "validation",
            b_changement = False,
            valide_nom = v_nom,
            valide_localisation = v_local,
            valide_description = v_descr
        )
    if identifiant:
        with bd.creer_connexion() as connexion:
            with connexion.get_curseur() as curseur:
                curseur.execute("SELECT ser.id_service FROM services ser")
                categories = curseur.execute("SELECT nom_categorie FROM categories")

                curseur.execute('SELECT cat.nom_categorie, ser.date_creation, ser.titre, ser.actif, ser.description, ser.cout, ser.localisation FROM services ser INNER JOIN categories cat ON cat.id_categorie = ser.id_service WHERE ser.id_service =%(id)s', {'id': identifiant})
                leservice = curseur.fetchone()
                if leservice.rowcount == 0:
                    abort(404, "le service à modifier n'existe pas")
                return render_template("changement.jinja",titre_page = "Modification service", b_changement=True, service=leservice, liste_categorie = categories)   
    return render_template("changement.jinja",titre_page = "Ajout service", b_changement=False, service=None, liste_categorie = categories)

@app.route("/services")
def services():
    """Affiche tous les services dans la base de données"""
    retour = []
    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            curseur.execute("SELECT id_service, (SELECT nom_categorie FROM `categories` WHERE categories.id_categorie = services.id_categorie), titre, localisation, description FROM `services` ORDER BY services.date_creation")
            retour = curseur.fetchall()
    print(retour)
    return render_template('services.jinja',titre_page = "Services", lesservices=retour)


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
    return render_template("erreur.jinja", message = e.description)

if __name__ == "__main__":
    app.run()
