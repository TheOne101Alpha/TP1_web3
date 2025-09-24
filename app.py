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


    return render_template('acceuil.jinja', titre=SITENOM, langue = "fr_CA", items=retour)

@app.route("/details")
def details():
    """affiche la page de détail"""

    retour = []
    identifiant = request.args.get('id', type=int)
    print(identifiant)

    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            curseur.execute('SELECT cat.nom_categorie,ser.titre, ser.actif, ser.description, ser.cout, ser.localisation FROM services ser INNER JOIN categories cat ON cat.id_categorie = ser.id_service WHERE ser.id_service =%(id)s', {'id': identifiant})
            retour = curseur.fetchone()

    print(retour)
    return render_template("details.jinja", item = retour, tiny = retour["actif"])



if __name__ == "__main__":
    app.run()
