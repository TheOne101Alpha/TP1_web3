from flask import Flask, render_template, request,abort
import bd



SITENOM = 'Services-TP1'

app = Flask(__name__)

@app.route('/')
def base():
    """Affiche la page d'acceuil du site"""
    retour = []
    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            curseur.execute("SELECT cat.nom_categorie,ser.id_service, ser.titre, ser.description, ser.cout, ser.localisation FROM services ser INNER JOIN categories cat ON cat.id_categorie = ser.id_service ORDER BY ser.date_creation LIMIT 5")
            retour = curseur.fetchall()
    return render_template('acceuil.jinja', titre=SITENOM, titre_page = "Acceuil", langue = "fr_CA", items=retour)

@app.route("/details")
def details():
    """affiche la page de détail"""

    retour = []
    identifiant = request.args.get('id', type=int)
    print(identifiant)

    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            curseur.execute('SELECT cat.nom_categorie, ser.date_creation, ser.titre, ser.actif, ser.description, ser.cout, ser.localisation FROM services ser INNER JOIN categories cat ON cat.id_categorie = ser.id_service WHERE ser.id_service =%(id)s', {'id': identifiant})
            retour = curseur.fetchone()
    return render_template("details.jinja",titre=SITENOM, titre_page = "Détails", item = retour, id_change = identifiant)


@app.route("/changement")
def changement():
    """affichage de changement ou ajout de services"""

    leservice = []
    categories = []

    identifiant = request.args.get('id', type=int)
    if identifiant:
        with bd.creer_connexion() as connexion:
            with connexion.get_curseur() as curseur:
                curseur.execute('SELECT cat.nom_categorie, ser.date_creation, ser.titre, ser.actif, ser.description, ser.cout, ser.localisation FROM services ser INNER JOIN categories cat ON cat.id_categorie = ser.id_service WHERE ser.id_service =%(id)s', {'id': identifiant})
                leservice = curseur.fetchone()
        print(leservice)
        return render_template("changement.jinja",titre=SITENOM,titre_page = "Modification service", b_changement=True, service=leservice, liste_categorie = categories )

    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            curseur.execute('SELECT id_categorie, nom_categorie FROM categories')
            categories = curseur.fetchall()
            curseur.execute('SELECT cat.nom_categorie, ser.date_creation, ser.titre, ser.actif, ser.description, ser.cout, ser.localisation FROM services ser INNER JOIN categories cat ON cat.id_categorie = ser.id_service WHERE ser.id_service =%(id)s', {'id': identifiant})
            services = curseur.fetchone()
    return render_template("changement.jinja",titre=SITENOM, titre_page = "Ajout service", b_changement = False, service = services, liste_categorie = categories)


@app.route("/services")
def services():
    """Affiche tous les services dans la base de données"""
    retour = []
    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            curseur.execute("SELECT id_service, (SELECT nom_categorie FROM `categories` WHERE categories.id_categorie = services.id_categorie), titre, localisation, description FROM `services` ORDER BY services.date_creation")
            retour = curseur.fetchall()
    print(retour)
    return render_template('services.jinja',titre=SITENOM,titre_page = "Services", lesservices=retour)


if __name__ == "__main__":
    app.run()
