from flask import Flask, render_template
import bd



SITENOM = 'Services-TP1'

app = Flask(__name__)

@app.route('/')
def base():
    """Affiche la page d'aceuil du site"""
    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            curseur.execute("SELECT cat.nom_categorie, ser.titre, ser.description, ser.cout FROM services ser INNER JOIN categories cat ON cat.id_categorie = ser.id_service ORDER BY ser.date_creation LIMIT 5")
            retour = curseur.fetchall()

    return render_template('acceuil.jinja', titre=SITENOM, langue = "fr_CA", list=retour)



if __name__ == "__main__":
    app.run()
